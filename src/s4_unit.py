"""Study 4 (plan study_plan_scale_v4_SEALED.md): one unit = (dataset, arm, seed, k).
arm: K20 / K50 (more clients, one owner per rare class) or own2 / own3 (K = 10, each rare class at 2 or 3 owners).
Same methods as Study 3 without DP experts and membership-inference sets. Saves float16 logits / margins;
analyze_s4.py applies calibration, metrics and the decision rules.
Usage: python3 s4_unit.py DATASET ARM SEED K OUTDIR
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np

import conf_fl
import pilot2_fl
import pilot_fl
import s3_unit

ALPHA = 0.5


def arm_cfg(arm):
    return (int(arm[1:]), 1) if arm.startswith("K") else (10, int(arm[3:]))


def make_clients_multi(y, part, rng, alpha, k, m):
    """pilot_fl.make_clients, except each rare class goes to m distinct owners, each with k disjoint labelled flows."""
    K = pilot_fl.K_CLIENTS; tr = np.where(part == "train")[0]
    ben = rng.choice(tr[y[tr] == 0], pilot_fl.N_BENIGN_TRAIN, replace=False)
    clients = [[] for _ in range(K)]
    for ci, c in enumerate(pilot_fl.CLASSES):
        if c in pilot_fl.RARE:
            continue
        idx = ben if c == "Benign" else tr[y[tr] == ci]
        share = rng.dirichlet([alpha] * K); cut = (np.cumsum(share) * len(idx)).astype(int)[:-1]
        for j, chunk in enumerate(np.split(rng.permutation(idx), cut)):
            clients[j].extend(chunk)
    owners = {}
    for c in pilot_fl.RARE:
        ci = pilot_fl.CLASSES.index(c); js = rng.choice(K, m, replace=False)
        sel = rng.choice(tr[y[tr] == ci], min(k * m, (y[tr] == ci).sum()), replace=False)
        for j, chunk in zip(js, np.array_split(sel, m)):
            clients[j].extend(chunk)
        owners[c] = [int(j) for j in js]
    return [np.array(c) for c in clients], owners


def run(ds, arm, seed, k, log):
    K, m = arm_cfg(arm)
    conf_fl.setup(ds, "primary"); pilot_fl.K_CLIENTS = K
    X, y, part, tt, _ = s3_unit.load_meta(ds); log("loaded")
    C = len(pilot_fl.CLASSES); E = 5; R = conf_fl.ROUNDS
    rng = np.random.default_rng(seed * 1000 + int(ALPHA * 100) + k + 100 * K + 10 * m)
    if pilot_fl.RARE[0] in ("ransomware", "SQL_Injection"):  # ToN and CIC: per-run cap of common attack train flows (as Study 3)
        part = part.copy(); r2 = np.random.default_rng(20_000 + seed)
        for ci in range(1, C - len(pilot_fl.RARE)):
            ix = np.where((part == "train") & (y == ci))[0]
            if len(ix) > conf_fl.TON_COMMON_TRAIN:
                part[r2.choice(ix, len(ix) - conf_fl.TON_COMMON_TRAIN, replace=False)] = "unused"
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    clients, owners = make_clients_multi(y, part, rng, ALPHA, k, m)
    te = np.where(part == "test")[0]
    ben = te[y[te] == 0]; ben = rng.choice(ben, min(len(ben), pilot_fl.N_BENIGN_TEST), replace=False)
    te = np.concatenate([ben, te[y[te] != 0]])
    rid = [pilot_fl.CLASSES.index(c) for c in pilot_fl.RARE]
    va = np.where((part == "val") & ~np.isin(y, rid))[0]
    cal = np.random.default_rng(10_000 + seed).choice(va, min(conf_fl.N_CAL, len(va)), replace=False)
    p0 = pilot_fl.init(X.shape[1], C, rng)
    n = np.stack([np.bincount(y[i], minlength=C) for i in clients]).astype(float); sizes = n.sum(1)
    Nc = n.sum(0); wg = np.where(Nc > 0, 1 / np.sqrt(np.maximum(Nc, 1)), 0); wg = (wg / (wg @ Nc / Nc.sum())).astype(np.float32)
    CW = [pilot2_fl.class_weights(y[i], C) for i in clients]
    lt = lambda p, j, **kw: pilot_fl.local_train(p, Z[clients[j]], y[clients[j]], rng, epochs=E, **kw)
    timing = {}

    def fl(kind):
        p = p0
        for _ in range(R):
            if kind == "FedAvg-bal":
                ups = [lt(p, j, cw=CW[j]) for j in range(K)]
            elif kind == "FedProx-bal":
                ups = [lt(p, j, cw=CW[j], mu=0.01, anchor=p) for j in range(K)]
            else:
                ups = [lt(p, j, cw=wg) for j in range(K)]
            p = pilot_fl.avg(ups, sizes)
            if kind == "GB+CR":
                for c in range(C):
                    h = np.where(n[:, c] > 0)[0]
                    if len(h):
                        w = n[h, c] / n[h, c].sum()
                        p["Wh"][:, c] = sum(wi * ups[j]["Wh"][:, c] for wi, j in zip(w, h))
                        p["bh"][c] = sum(wi * ups[j]["bh"][c] for wi, j in zip(w, h))
        return p
    models = {}
    for kd in ("FedAvg-bal", "FedProx-bal", "GB+CR"):
        t0 = time.time(); models[kd] = fl(kd)
        if kd == "FedAvg-bal":
            models["CCVR"] = pilot2_fl.ccvr(models[kd], Z, y, clients, C, rng)
        timing[kd] = time.time() - t0; log(f"  {kd} {timing[kd]:.0f}s")
    allidx = np.concatenate(clients)
    models["Central-bal"] = pilot_fl.local_train(p0, Z[allidx], y[allidx], rng, epochs=R, cw=pilot2_fl.class_weights(y[allidx], C))
    lg = lambda p, idx: pilot_fl.forward(p, Z[idx])[3].astype(np.float32)
    h16 = lambda a: a.astype(np.float16)
    neg = [clients[j][~np.isin(y[clients[j]], rid)] for j in range(K)]; negall = np.concatenate(neg)
    out = {"y_test": y[te], "t_test": tt[te], "classes": np.array(pilot_fl.CLASSES), "rare": np.array(pilot_fl.RARE),
           "owners": np.array([owners[c] for c in pilot_fl.RARE]), "neg_sizes": np.array([len(i) for i in neg]),
           "client_sizes": sizes, "K": K, "m": m}
    for mname in ("CCVR", "FedProx-bal", "GB+CR", "Central-bal"):
        out[f"{mname}|test"] = h16(lg(models[mname], te)); out[f"{mname}|cal"] = h16(lg(models[mname], cal))
    t0 = time.time()
    for c, ci in zip(pilot_fl.RARE, rid):
        for o, j in enumerate(owners[c]):
            idx = clients[j]; pe = pilot_fl.local_train(p0, Z[idx], y[idx], rng, epochs=R, cw=CW[j])
            Lt = lg(pe, te)
            out[f"expert_{c}_o{o}|test"] = s3_unit.margin(Lt, ci); out[f"expert_{c}_o{o}|negall"] = s3_unit.margin(lg(pe, negall), ci)
            out[f"expert_{c}_o{o}|argmax_is_c"] = Lt.argmax(1) == ci
    timing["experts"] = time.time() - t0; log(f"  experts {timing['experts']:.0f}s")
    for name, fn in (("FedOV", None), ("FedOV-full", s3_unit.fedov_full_local)):
        t0 = time.time(); locs = []
        for i in clients:
            Xi, yi = Z[i], y[i]
            if fn is None:
                import pilot6_baselines
                sub = rng.choice(len(i), max(1, len(i) // 2), replace=False)
                Xa = np.concatenate([Xi, pilot6_baselines.destroy(Xi[sub], rng)]); ya = np.concatenate([yi, np.full(len(sub), C)])
                locs.append(pilot_fl.local_train(pilot_fl.init(X.shape[1], C + 1, rng), Xa, ya, rng, epochs=R, cw=pilot2_fl.class_weights(ya, C + 1)))
            else:
                locs.append(fn(Xi, yi, C, rng, R))
        a, b = s3_unit.softmax_sum(locs, Z, [te, cal]); out[f"{name}|test"], out[f"{name}|cal"] = h16(a), h16(b)
        timing[name] = time.time() - t0; log(f"  {name} {timing[name]:.0f}s")
    out["timing_names"] = np.array(list(timing)); out["timing_secs"] = np.array(list(timing.values()))
    return out


if __name__ == "__main__":
    ds, arm, seed, k, outdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    f = os.path.join(outdir, f"{ds}_{arm}_s{seed}_k{k}.npz")
    if os.path.exists(f):
        sys.exit(0)
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {ds} {arm} s{seed} k{k} {s}", flush=True)
    res = run(ds, arm, seed, k, log)
    np.savez_compressed(f + ".tmp.npz", **res); os.replace(f + ".tmp.npz", f); log("finished")

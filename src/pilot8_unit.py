"""Pilot 8 (development seeds 0-4 only; exploratory, no claims): candidate parts of a Study 5.
Saves raw scores so that analyze_pilot8.py can try the calibration variants offline:
  - plain owner expert (as SAFE-X) and a frozen-encoder expert (global GB+CR encoder frozen, head trained at the owner);
  - margins on all clients' non-rare training flows (negall) with their labels, for pooled and per-group calibration;
  - test margins with labels and timestamps, for online (adaptive conformal) calibration on the time-ordered test stream;
  - GB+CR and FedOV / FedOV-full logits on test and validation-calibration flows.
Setting as Study 3 main arm: K = 10, one owner per rare class, k = 20, alpha = 0.5.
Usage: python3 pilot8_unit.py DATASET SEED OUTDIR
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
import s4_unit

K, K_SHOTS, ALPHA = 10, 20, 0.5


def run(ds, seed, log):
    conf_fl.setup(ds, "primary"); pilot_fl.K_CLIENTS = K
    X, y, part, tt, _ = s3_unit.load_meta(ds); log("loaded")
    C = len(pilot_fl.CLASSES); E = 5; R = conf_fl.ROUNDS
    rng = np.random.default_rng(seed * 1000 + 50 + K_SHOTS + 8888)
    if pilot_fl.RARE[0] in ("ransomware", "SQL_Injection"):
        part = part.copy(); r2 = np.random.default_rng(20_000 + seed)
        for ci in range(1, C - len(pilot_fl.RARE)):
            ix = np.where((part == "train") & (y == ci))[0]
            if len(ix) > conf_fl.TON_COMMON_TRAIN:
                part[r2.choice(ix, len(ix) - conf_fl.TON_COMMON_TRAIN, replace=False)] = "unused"
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6; Z = (X - mu_) / sd_
    clients, owners = s4_unit.make_clients_multi(y, part, rng, ALPHA, K_SHOTS, 1)
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
    lg = lambda p, idx: pilot_fl.forward(p, Z[idx])[3].astype(np.float32)
    h16 = lambda a: np.asarray(a).astype(np.float16)
    timing = {}
    t0 = time.time(); p = p0
    for _ in range(R):
        ups = [pilot_fl.local_train(p, Z[clients[j]], y[clients[j]], rng, epochs=E, cw=wg) for j in range(K)]
        p = pilot_fl.avg(ups, sizes)
        for c in range(C):
            h = np.where(n[:, c] > 0)[0]
            if len(h):
                w = n[h, c] / n[h, c].sum()
                p["Wh"][:, c] = sum(wi * ups[j]["Wh"][:, c] for wi, j in zip(w, h)); p["bh"][c] = sum(wi * ups[j]["bh"][c] for wi, j in zip(w, h))
    gb = p; timing["GB+CR"] = time.time() - t0; log(f"  GB+CR {timing['GB+CR']:.0f}s")
    neg = [clients[j][~np.isin(y[clients[j]], rid)] for j in range(K)]; negall = np.concatenate(neg)
    out = {"y_test": y[te], "t_test": tt[te], "classes": np.array(pilot_fl.CLASSES), "rare": np.array(pilot_fl.RARE),
           "owners": np.array([owners[c][0] for c in pilot_fl.RARE]), "neg_sizes": np.array([len(i) for i in neg]),
           "y_negall": y[negall], "t_negall": tt[negall], "GB+CR|test": h16(lg(gb, te)), "GB+CR|cal": h16(lg(gb, cal))}
    t0 = time.time()
    for c, ci in zip(pilot_fl.RARE, rid):
        o = owners[c][0]; idx = clients[o]
        experts = {"plain": pilot_fl.local_train(p0, Z[idx], y[idx], rng, epochs=R, cw=CW[o]),
                   "frozen": pilot_fl.local_train(gb, Z[idx], y[idx], rng, epochs=R, cw=CW[o], train={"Wh", "bh"})}
        for name, pe in experts.items():
            Lt = lg(pe, te)
            out[f"{name}_{c}|test"] = s3_unit.margin(Lt, ci); out[f"{name}_{c}|negall"] = s3_unit.margin(lg(pe, negall), ci)
            out[f"{name}_{c}|owner_argmax"] = Lt.argmax(1) == ci
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
    ds, seed, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    f = os.path.join(outdir, f"{ds}_s{seed}.npz")
    if os.path.exists(f):
        sys.exit(0)
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {ds} s{seed} {s}", flush=True)
    res = run(ds, seed, log)
    np.savez_compressed(f + ".tmp.npz", **res); os.replace(f + ".tmp.npz", f); log("finished")

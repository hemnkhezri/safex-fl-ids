"""Study 3 (plan study_plan_robustness_v3_SEALED.md): one unit = (dataset, arm, seed, k).
arm: main (Dirichlet sites, 45-64-32), ip (destination-host sites, ToN only), big (45-256-128, k = 20).
Saves logits / scores; analyze_s3.py applies calibration, metrics and the decision rules.
Usage: python3 s3_unit.py DATASET ARM SEED K OUTDIR
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np
import pandas as pd
import logging

logging.getLogger("absl").setLevel(logging.ERROR)

import conf_fl
import pilot2_fl
import pilot_fl
import pilot6_baselines

ALPHA = 0.5
CACHE = os.environ.get("SAFEX_CACHE", os.path.expanduser("~/.cache/safex"))


# ------------------------------------------------------------------ data with time and destination host
def load_meta(ds):
    f = os.path.join(CACHE, f"{ds}_meta.npz")
    if os.path.exists(f):
        z = np.load(f, allow_pickle=True)
        return z["X"], z["y"], z["part"], z["t"], z["dst"]
    if ds == "unsw":
        df = pd.read_parquet(pilot_fl.DATA).sort_values("FLOW_START_MILLISECONDS").reset_index(drop=True)
        n = len(df); part = np.empty(n, dtype=object)
        part[: int(0.7 * n)] = "train"; part[int(0.7 * n): int(0.8 * n)] = "val"; part[int(0.8 * n):] = "test"
        y = df.Attack.map({c: i for i, c in enumerate(pilot_fl.CLASSES)}).to_numpy()
    else:
        df = pd.read_parquet(conf_fl.CIC_POOL if ds == "cic" else conf_fl.TON_POOL)
        part = df.pop("part").to_numpy().astype(object)
        y = df.Attack.astype(str).map({c: i for i, c in enumerate(pilot_fl.CLASSES)}).to_numpy()
    X = df.drop(columns=pilot_fl.DROP).astype("float64").replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.max())
    X["DST_PORT_WELLKNOWN"] = (df.L4_DST_PORT < 1024).astype(float)
    X = np.log1p(X.clip(lower=0)).to_numpy(np.float32)
    key = pd.util.hash_pandas_object(pd.DataFrame(X), index=False).to_numpy()
    keep = ~((part == "test") & np.isin(key, key[part == "train"]))
    t = df.FLOW_START_MILLISECONDS.to_numpy(np.int64); dst = df.IPV4_DST_ADDR.astype(str).to_numpy()
    out = dict(X=X[keep], y=y[keep], part=part[keep], t=t[keep], dst=dst[keep])
    os.makedirs(CACHE, exist_ok=True); np.savez(f + ".tmp.npz", **out); os.replace(f + ".tmp.npz", f)
    return out["X"], out["y"], out["part"], out["t"], out["dst"]


def make_clients_ip(y, part, dst, rng, k):
    """Sites = groups of destination hosts, balanced by training-flow count (plan v3 Part B)."""
    K = pilot_fl.K_CLIENTS; R = [pilot_fl.CLASSES.index(c) for c in pilot_fl.RARE]
    tr = np.where(part == "train")[0]
    ben = tr[y[tr] == 0]; keep_ben = rng.choice(ben, pilot_fl.N_BENIGN_TRAIN, replace=False)
    pool = np.concatenate([keep_ben, tr[(y[tr] != 0)]])
    hosts, inv = np.unique(dst[pool], return_inverse=True); cnt = np.bincount(inv)
    order = rng.permutation(len(hosts)); site_of = np.zeros(len(hosts), int); load = np.zeros(K)
    for h in order:
        s = int(load.argmin()); site_of[h] = s; load[s] += cnt[h]
    site = site_of[inv]
    clients = [list(pool[(site == j) & ~np.isin(y[pool], R)]) for j in range(K)]
    owner, n_used = {}, {}
    for c in pilot_fl.RARE:
        ci = pilot_fl.CLASSES.index(c); m = y[pool] == ci
        j = int(np.bincount(site[m], minlength=K).argmax()); idx = pool[m & (site == j)]
        sel = rng.choice(idx, min(k, len(idx)), replace=False); clients[j].extend(sel); owner[c] = j; n_used[c] = len(sel)
    return [np.array(c) for c in clients], owner, n_used


def margin(L, c):
    o = L.copy(); o[:, c] = -np.inf
    return (L[:, c] - o.max(1)).astype(np.float32)


# ------------------------------------------------------------------ DP-SGD expert
def dp_sigma(q, steps, eps, delta=1e-5):
    import dp_accounting as dpa
    from dp_accounting.rdp import rdp_privacy_accountant as rdp

    def e(s):
        a = rdp.RdpAccountant(); a.compose(dpa.PoissonSampledDpEvent(q, dpa.GaussianDpEvent(s)), steps)
        return a.get_epsilon(delta)
    lo, hi = 0.3, 50.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if e(mid) > eps else (lo, mid)
    return hi


def dp_train(p, X, y, cw, rng, eps, epochs=60, B=256, clip=1.0, lr=0.05):
    p = {k: v.copy() for k, v in p.items()}; N = len(X); q = min(1.0, B / N); steps = int(epochs * N / B)
    sigma = dp_sigma(q, steps, eps)
    for _ in range(steps):
        b = np.where(rng.random(N) < q)[0]
        g = {k: np.zeros_like(v) for k, v in p.items()}
        if len(b):
            xb, yb = X[b], y[b]
            a1, z1, h, lo = pilot_fl.forward(p, xb)
            lo = lo - lo.max(1, keepdims=True); pr = np.exp(lo); pr /= pr.sum(1, keepdims=True)
            gl = pr; gl[np.arange(len(b)), yb] -= 1; gl *= cw[yb][:, None]
            gh = gl @ p["Wh"].T; gz = gh @ p["W2"].T; ga = gz * (a1 > 0)
            sq = lambda u: (u ** 2).sum(1)
            nrm = np.sqrt(sq(h) * sq(gl) + sq(gl) + sq(z1) * sq(gh) + sq(gh) + sq(xb) * sq(ga) + sq(ga))
            f = np.minimum(1.0, clip / (nrm + 1e-12))[:, None]
            gl, gh, ga = gl * f, gh * f, ga * f
            g = {"Wh": h.T @ gl, "bh": gl.sum(0), "W2": z1.T @ gh, "b2": gh.sum(0), "W1": xb.T @ ga, "b1": ga.sum(0)}
        for k in p:
            p[k] -= lr * (g[k] + rng.normal(0, sigma * clip, g[k].shape).astype(np.float32)) / B
    return p, sigma


# ------------------------------------------------------------------ FedOV-full local model
def fedov_full_local(Xi, yi, C, rng, epochs):
    d = Xi.shape[1]; p = pilot_fl.init(d, C + 1, rng)
    sub = rng.choice(len(Xi), max(1, len(Xi) // 2), replace=False); D = pilot6_baselines.destroy(Xi[sub], rng)
    for _ in range(epochs):
        a = rng.choice(len(Xi), max(1, len(Xi) // 4), replace=False)  # FGSM unknowns from the current model
        a1, z1, h, lo = pilot_fl.forward(p, Xi[a])
        lo = lo - lo.max(1, keepdims=True); pr = np.exp(lo); pr /= pr.sum(1, keepdims=True); pr[np.arange(len(a)), yi[a]] -= 1
        gx = (((pr @ p["Wh"].T) @ p["W2"].T) * (a1 > 0)) @ p["W1"].T
        A = Xi[a] + 0.5 * np.sign(gx).astype(np.float32)
        i1 = rng.integers(0, len(Xi), len(Xi) // 4); i2 = rng.integers(0, len(Xi), len(Xi) // 4)
        ok = yi[i1] != yi[i2]; lam = rng.uniform(0.3, 0.7, (ok.sum(), 1)).astype(np.float32)
        M = lam * Xi[i1[ok]] + (1 - lam) * Xi[i2[ok]]
        Xa = np.concatenate([Xi, D, A, M]); ya = np.concatenate([yi, np.full(len(D) + len(A) + len(M), C)])
        p = pilot_fl.local_train(p, Xa, ya, rng, epochs=1, cw=pilot2_fl.class_weights(ya, C + 1))
    return p


def softmax_sum(models, Z, idx_list):
    outs = []
    for idx in idx_list:
        S = 0
        for pi in models:
            lo = pilot_fl.forward(pi, Z[idx])[3]; lo = lo - lo.max(1, keepdims=True); pr = np.exp(lo); S = S + pr / pr.sum(1, keepdims=True)
        outs.append(np.log(S[:, :-1] + 1e-9).astype(np.float32))
    return outs


# ------------------------------------------------------------------ one unit
def run(ds, arm, seed, k, log):
    conf_fl.setup(ds, "big" if arm == "big" else "primary")
    if arm == "big":
        pilot_fl.HID, pilot_fl.EMB = 256, 128; pilot2_fl.EMB = 128
    X, y, part, tt, dst = load_meta(ds); log("loaded")
    C = len(pilot_fl.CLASSES); E = 5; R = conf_fl.ROUNDS
    rng = np.random.default_rng(seed * 1000 + int(ALPHA * 100) + k + {"main": 0, "ip": 7, "big": 13}[arm])
    if pilot_fl.RARE[0] in ("ransomware", "SQL_Injection"):  # ToN and CIC: per-run cap of common attack train flows
        part = part.copy(); r2 = np.random.default_rng(20_000 + seed)
        for ci in range(1, C - len(pilot_fl.RARE)):
            ix = np.where((part == "train") & (y == ci))[0]
            if len(ix) > conf_fl.TON_COMMON_TRAIN:
                part[r2.choice(ix, len(ix) - conf_fl.TON_COMMON_TRAIN, replace=False)] = "unused"
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    if arm == "ip":
        clients, owner, n_used = make_clients_ip(y, part, dst, rng, k)
    else:
        clients, owner = pilot_fl.make_clients(Z, y, part, rng, ALPHA, k, 1.0); n_used = {c: k for c in pilot_fl.RARE}
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
                ups = [lt(p, j, cw=CW[j]) for j in range(len(clients))]
            elif kind == "FedProx-bal":
                ups = [lt(p, j, cw=CW[j], mu=0.01, anchor=p) for j in range(len(clients))]
            else:
                ups = [lt(p, j, cw=wg) for j in range(len(clients))]
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
    allidx = np.concatenate(clients); t0 = time.time()
    models["Central-bal"] = pilot_fl.local_train(p0, Z[allidx], y[allidx], rng, epochs=R, cw=pilot2_fl.class_weights(y[allidx], C))
    timing["Central-bal"] = time.time() - t0
    lg = lambda p, idx: pilot_fl.forward(p, Z[idx])[3].astype(np.float32)
    neg = [clients[j][~np.isin(y[clients[j]], rid)] for j in range(len(clients))]; negall = np.concatenate(neg)
    used = np.zeros(len(y), bool); used[allidx] = True
    out = {"y_test": y[te], "t_test": tt[te], "classes": np.array(pilot_fl.CLASSES), "rare": np.array(pilot_fl.RARE),
           "owner": np.array([owner[c] for c in pilot_fl.RARE]), "n_used": np.array([n_used[c] for c in pilot_fl.RARE]),
           "neg_sizes": np.array([len(i) for i in neg]), "client_sizes": sizes}
    for m in ("CCVR", "FedProx-bal", "GB+CR", "Central-bal"):
        out[f"{m}|test"] = lg(models[m], te); out[f"{m}|cal"] = lg(models[m], cal)
    # owner experts: non-private and DP (epsilon 1, 8); membership-inference sets
    t0 = time.time()
    for c, ci in zip(pilot_fl.RARE, rid):
        j = owner[c]; idx = clients[j]
        mem = idx[y[idx] == ci]
        pool_nm = np.where((part == "train") & (y == ci) & ~used)[0]
        nonmem = rng.choice(pool_nm, min(len(mem), len(pool_nm)), replace=False) if len(pool_nm) else np.array([], int)
        variants = {"": pilot_fl.local_train(p0, Z[idx], y[idx], rng, epochs=R, cw=CW[j])}
        for eps in (1, 8):
            variants[f"dp{eps}"], out[f"sigma_{c}_dp{eps}"] = dp_train(p0, Z[idx], y[idx], CW[j], rng, eps, epochs=R)
        for v, pe in variants.items():
            tag = f"expert{('_' + v) if v else ''}_{c}"
            mg = lambda idx: margin(lg(pe, idx), ci) if len(idx) else np.zeros(0, np.float32)
            out[f"{tag}|test"] = mg(te); out[f"{tag}|negall"] = mg(negall)  # margin s_c only (saves space)
            out[f"{tag}|mem"] = mg(mem); out[f"{tag}|nonmem"] = mg(nonmem)
            if not v:
                out[f"{tag}|argmax_is_c"] = lg(pe, te).argmax(1) == ci
    timing["experts (incl. DP)"] = time.time() - t0; log(f"  experts {timing['experts (incl. DP)']:.0f}s")
    # FedOV-tab and FedOV-full
    for name, fn in (("FedOV", None), ("FedOV-full", fedov_full_local)):
        t0 = time.time(); locs = []
        for i in clients:
            Xi, yi = Z[i], y[i]
            if fn is None:
                sub = rng.choice(len(i), max(1, len(i) // 2), replace=False)
                Xa = np.concatenate([Xi, pilot6_baselines.destroy(Xi[sub], rng)]); ya = np.concatenate([yi, np.full(len(sub), C)])
                locs.append(pilot_fl.local_train(pilot_fl.init(X.shape[1], C + 1, rng), Xa, ya, rng, epochs=R, cw=pilot2_fl.class_weights(ya, C + 1)))
            else:
                locs.append(fn(Xi, yi, C, rng, R))
        out[f"{name}|test"], out[f"{name}|cal"] = softmax_sum(locs, Z, [te, cal])
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

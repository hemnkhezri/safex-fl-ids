"""Pilot 6 (development): the two baselines the literature check makes mandatory, on the same clients/test sets as
pilot 5 (identical rng sequence up to the test/calibration draws).
- PROTEAN (Saidi et al., ESORICS 2025, arXiv 2507.05524): FedAvg + proximal term (mu = 0.1) + alignment of
  embeddings to global class prototypes (uniform mean over clients holding the class); inference by nearest global
  prototype. Plain CE as in the paper. R = 60, E = 5 (our budget, not the paper's 10 x 3).
- FedOV-tab (Diao et al., ICLR 2023), adapted to tabular data: each client trains once (60 epochs) a C+1-way model
  whose extra class is "unknown", fed with destroyed copies of its own flows (feature mixing across rows, Gaussian
  noise on half the features, half-vector swap; 50% of local size). Server: sum of softmax over clients, unknown
  channel dropped, argmax. The adversarial (FGSM) outlier step and PROSER terms are omitted (documented simplification).
Saves logits to results/pilot6/{ds}_s{seed}_k{k}.npz.
Usage: python3 pilot6_baselines.py DATASET SEED K OUTDIR
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np

import conf_fl
import pilot2_fl
import pilot_fl

ALPHA = 0.5


def destroy(X, rng):
    n, d = X.shape; out = X.copy(); op = rng.integers(0, 3, n)
    m = op == 0  # mix: half the features taken from other random rows
    if m.any():
        cols = rng.random((m.sum(), d)) < 0.5
        out[m] = np.where(cols, X[rng.integers(0, n, m.sum())], X[m])
    m = op == 1  # strong noise on half the features
    if m.any():
        cols = rng.random((m.sum(), d)) < 0.5
        out[m] = X[m] + cols * rng.normal(0, 2.0, (m.sum(), d)).astype(np.float32)
    m = op == 2  # swap the two halves of the feature vector
    if m.any():
        h = d // 2; out[m] = np.concatenate([X[m][:, d - h:], X[m][:, h:d - h], X[m][:, :h]], 1)
    return out


def run(X, y, part, seed, k, log):
    C = len(pilot_fl.CLASSES); R = conf_fl.ROUNDS
    rng = np.random.default_rng(seed * 1000 + int(ALPHA * 100) + k)
    if pilot_fl.RARE[0] == "ransomware":
        part = part.copy(); r2 = np.random.default_rng(20_000 + seed)
        for ci in range(1, C - len(pilot_fl.RARE)):
            ix = np.where((part == "train") & (y == ci))[0]
            if len(ix) > conf_fl.TON_COMMON_TRAIN:
                part[r2.choice(ix, len(ix) - conf_fl.TON_COMMON_TRAIN, replace=False)] = "unused"
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    clients, owner = pilot_fl.make_clients(Z, y, part, rng, ALPHA, k, 1.0)
    te = np.where(part == "test")[0]
    ben = te[y[te] == 0]; ben = rng.choice(ben, min(len(ben), pilot_fl.N_BENIGN_TEST), replace=False)
    te = np.concatenate([ben, te[y[te] != 0]])
    rid = [pilot_fl.CLASSES.index(c) for c in pilot_fl.RARE]
    va = np.where((part == "val") & ~np.isin(y, rid))[0]
    cal = np.random.default_rng(10_000 + seed).choice(va, min(conf_fl.N_CAL, len(va)), replace=False)
    rng = np.random.default_rng(50_000 + seed * 1000 + k)  # fresh stream for the new methods
    d = X.shape[1]; n = np.stack([np.bincount(y[i], minlength=C) for i in clients]).astype(float); sizes = n.sum(1)
    out = {"y_test": y[te]}
    # PROTEAN
    t0 = time.time(); p = pilot_fl.init(d, C, rng); G = None
    for _ in range(R):
        ups = [pilot_fl.local_train(p, Z[i], y[i], rng, epochs=5, protos=G, mu=0.1, anchor=p) for i in clients]
        stats = [pilot_fl.local_stats(u, Z[i], y[i], C) for u, i in zip(ups, clients)]
        P = np.stack([s[0] for s in stats]); ok = ~np.isnan(P[:, :, 0])
        G = np.where(ok.any(0)[:, None], np.nansum(np.where(ok[:, :, None], P, 0), 0) / np.maximum(ok.sum(0), 1)[:, None], np.nan)
        p = pilot_fl.avg(ups, sizes)
    h = pilot_fl.embed(p, Z[te]); okc = ~np.isnan(G[:, 0])
    dist = ((h[:, None, :] - G[None, okc, :]) ** 2).sum(2)
    out["PROTEAN|test_pred"] = np.where(okc)[0][dist.argmin(1)]
    out["PROTEAN|test"] = -np.full((len(te), C), np.inf, np.float32); out["PROTEAN|test"][:, okc] = -dist
    hc = pilot_fl.embed(p, Z[cal]); out["PROTEAN|cal"] = -np.full((len(cal), C), np.inf, np.float32)
    out["PROTEAN|cal"][:, okc] = -((hc[:, None, :] - G[None, okc, :]) ** 2).sum(2)
    log(f"  PROTEAN {time.time() - t0:.0f}s")
    # FedOV-tab
    t0 = time.time(); S_te = np.zeros((len(te), C + 1)); S_cal = np.zeros((len(cal), C + 1))
    for i in clients:
        Xi, yi = Z[i], y[i]
        sub = rng.choice(len(i), max(1, len(i) // 2), replace=False)
        Xa = np.concatenate([Xi, destroy(Xi[sub], rng)]); ya = np.concatenate([yi, np.full(len(sub), C)])
        cw = pilot2_fl.class_weights(ya, C + 1)
        pi = pilot_fl.local_train(pilot_fl.init(d, C + 1, rng), Xa, ya, rng, epochs=R, cw=cw)
        for S, idx in ((S_te, te), (S_cal, cal)):
            lo = pilot_fl.forward(pi, Z[idx])[3]; lo = lo - lo.max(1, keepdims=True); pr = np.exp(lo); pr /= pr.sum(1, keepdims=True)
            S += pr
    out["FedOV|test"] = np.log(S_te[:, :C] + 1e-9).astype(np.float32); out["FedOV|cal"] = np.log(S_cal[:, :C] + 1e-9).astype(np.float32)
    log(f"  FedOV {time.time() - t0:.0f}s")
    return out


if __name__ == "__main__":
    ds, seed, k, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    f = os.path.join(outdir, f"{ds}_s{seed}_k{k}.npz")
    if os.path.exists(f):
        sys.exit(0)
    os.makedirs(outdir, exist_ok=True); conf_fl.setup(ds, "primary")
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {ds} s{seed} k{k} {s}", flush=True)
    X, y, part = conf_fl.load(ds); log("loaded")
    res = run(X, y, part, seed, k, log)
    np.savez_compressed(f + ".tmp.npz", **res); os.replace(f + ".tmp.npz", f); log("finished")

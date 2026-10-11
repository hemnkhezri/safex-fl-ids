"""Pilot 4 (development, not sealed): step 4 of method_design_v1.md, owner-calibrated rare-class decision.
Trains FedAvg-bal (+CCVR), GB+CR and Central-bal exactly as pilot 3c (E=5, R=60, alpha=0.5) and saves logits,
so thresholds can be studied post hoc (analyze_pilot4.py) without retraining:
- test set (same construction as pilot 3), with labels;
- a calibration sample of the validation period (time-ordered 70-80% slice, never used for training or test),
  rare classes removed: the "local benign/other traffic" a rare-class owner would calibrate on;
- each owner's own non-rare training flows (in-sample; reported as the naive calibration variant).
Usage: python3 pilot4_fl.py SEED OUTDIR
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np

import pilot_fl
from pilot_fl import CLASSES, N_BENIGN_TEST, RARE, avg, forward, init, load, make_clients
from pilot2_fl import ccvr, class_weights

ROUNDS, EPOCHS, ALPHA, N_CAL = 60, 5, 0.5, 20000


def local_train(*a, **kw):
    kw.setdefault("epochs", EPOCHS)
    return pilot_fl.local_train(*a, **kw)


def logits(p, X):
    return forward(p, X)[3].astype(np.float32)


def run(X, y, part, seed, k, log):
    rng = np.random.default_rng(seed * 1000 + int(ALPHA * 100) + k)  # same draws as pilots 3/3c
    C = len(CLASSES); d = X.shape[1]
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    clients, owner = make_clients(Z, y, part, rng, ALPHA, k, 1.0)
    te = np.where(part == "test")[0]
    ben_te = rng.choice(te[y[te] == 0], N_BENIGN_TEST, replace=False)
    te = np.concatenate([ben_te, te[y[te] != 0]])
    rare_ids = [CLASSES.index(c) for c in RARE]
    va = np.where((part == "val") & ~np.isin(y, rare_ids))[0]
    cal = np.random.default_rng(10_000 + seed).choice(va, N_CAL, replace=False)
    p0 = init(d, C, rng)
    n = np.stack([np.bincount(y[idx], minlength=C) for idx in clients]).astype(float)
    Nc = n.sum(0); wg = np.where(Nc > 0, 1 / np.sqrt(np.maximum(Nc, 1)), 0)
    wg = (wg / (wg @ Nc / Nc.sum())).astype(np.float32)
    CWl = [class_weights(y[idx], C) for idx in clients]
    sizes = n.sum(1)

    def fl(gb_cr):
        p = p0
        for _ in range(ROUNDS):
            ups = [local_train(p, Z[idx], y[idx], rng, cw=wg if gb_cr else CWl[j]) for j, idx in enumerate(clients)]
            p = avg(ups, sizes)
            if gb_cr:
                for c in range(C):
                    h = np.where(n[:, c] > 0)[0]
                    if len(h):
                        w = n[h, c] / n[h, c].sum()
                        p["Wh"][:, c] = sum(wi * ups[j]["Wh"][:, c] for wi, j in zip(w, h))
                        p["bh"][c] = sum(wi * ups[j]["bh"][c] for wi, j in zip(w, h))
        return p

    models = {}
    t0 = time.time(); models["FedAvg-bal"] = fl(False); models["CCVR"] = ccvr(models["FedAvg-bal"], Z, y, clients, C, rng)
    log(f"  FedAvg-bal+CCVR {time.time() - t0:.0f}s")
    t0 = time.time(); models["GB+CR"] = fl(True); log(f"  GB+CR {time.time() - t0:.0f}s")
    allidx = np.concatenate(clients)
    models["Central-bal"] = local_train(p0, Z[allidx], y[allidx], rng, epochs=ROUNDS, cw=class_weights(y[allidx], C))
    out = {"y_test": y[te], "y_cal": y[cal], "owner": np.array([owner[c] for c in RARE])}
    for c in RARE:
        idx = clients[owner[c]]; idx = idx[~np.isin(y[idx], rare_ids)]
        out[f"own_idx_{c}"] = idx
    for m, p in models.items():
        out[f"{m}|test"] = logits(p, Z[te]); out[f"{m}|cal"] = logits(p, Z[cal])
        for c in RARE:
            out[f"{m}|own_{c}"] = logits(p, Z[out[f"own_idx_{c}"]])
    return out


if __name__ == "__main__":
    SEED, OUTDIR = int(sys.argv[1]), sys.argv[2]
    os.makedirs(OUTDIR, exist_ok=True)
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)
    X, y, part, _ = load()
    for k in (20, 100):
        f = os.path.join(OUTDIR, f"seed{SEED}_k{k}.npz")
        if os.path.exists(f):
            continue
        log(f"seed={SEED} alpha={ALPHA} k={k}")
        res = run(X, y, part, SEED, k, log)
        np.savez_compressed(f, **{k_: v for k_, v in res.items() if not k_.startswith("own_idx")})
    log("finished")

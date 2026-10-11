"""Pilot 5 (development, not sealed): owner experts shared through the federation, with federated calibration.
Idea (user chose "new method", 2026-10-11): the confirmatory study showed the owner's local model beats every
federated method on its exclusive class. So each owner trains a local expert, shares only its parameters, and the
expert's threshold is set on the score distribution of ALL clients' local traffic (federated quantile), so it
controls false alarms on traffic the owner never saw. Prediction = expert hits override the global model.
Development seeds 0-4 only (confirmatory seeds 100-109 untouched for this method).
Saves logits; analyze_pilot5.py does calibration and scoring.
Usage: python3 pilot5_expert.py DATASET SEED K OUTDIR
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


def run(X, y, part, seed, k, log):
    C = len(pilot_fl.CLASSES); E = 5; R = conf_fl.ROUNDS
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
    p0 = pilot_fl.init(X.shape[1], C, rng)
    n = np.stack([np.bincount(y[i], minlength=C) for i in clients]).astype(float); sizes = n.sum(1)
    Nc = n.sum(0); wg = np.where(Nc > 0, 1 / np.sqrt(np.maximum(Nc, 1)), 0)
    wg = (wg / (wg @ Nc / Nc.sum())).astype(np.float32)
    CW = [pilot2_fl.class_weights(y[i], C) for i in clients]
    lt = lambda p, j, **kw: pilot_fl.local_train(p, Z[clients[j]], y[clients[j]], rng, epochs=E, **kw)

    def fl(kind):
        p = p0
        for _ in range(R):
            if kind == "FedAvg-bal":
                ups = [lt(p, j, cw=CW[j]) for j in range(len(clients))]
            elif kind == "FedProx-bal":
                ups = [lt(p, j, cw=CW[j], mu=0.01, anchor=p) for j in range(len(clients))]
            else:  # GB+CR
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
        log(f"  {kd} {time.time() - t0:.0f}s")
    allidx = np.concatenate(clients)
    models["Central-bal"] = pilot_fl.local_train(p0, Z[allidx], y[allidx], rng, epochs=R,
                                                 cw=pilot2_fl.class_weights(y[allidx], C))
    lg = lambda p, idx: pilot_fl.forward(p, Z[idx])[3].astype(np.float32)
    # every client's non-rare training flows: the traffic used for federated calibration
    neg = [clients[j][~np.isin(y[clients[j]], rid)] for j in range(len(clients))]
    out = {"y_test": y[te], "classes": np.array(pilot_fl.CLASSES), "rare": np.array(pilot_fl.RARE),
           "owner": np.array([owner[c] for c in pilot_fl.RARE]), "neg_sizes": np.array([len(i) for i in neg])}
    for m in ("CCVR", "FedProx-bal", "GB+CR", "Central-bal"):
        out[f"{m}|test"] = lg(models[m], te); out[f"{m}|cal"] = lg(models[m], cal)
    t0 = time.time()
    for c in pilot_fl.RARE:  # owner expert = owner's local class-balanced model (as Local-owner-bal)
        j = owner[c]; idx = clients[j]
        pe = pilot_fl.local_train(p0, Z[idx], y[idx], rng, epochs=R, cw=CW[j])
        out[f"expert_{c}|test"] = lg(pe, te); out[f"expert_{c}|cal"] = lg(pe, cal)
        out[f"expert_{c}|negall"] = lg(pe, np.concatenate(neg))
    log(f"  experts {time.time() - t0:.0f}s")
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

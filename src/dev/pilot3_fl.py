"""Pilot 3 (design-stage development, not sealed): which existing ingredients close the client-exclusive gap?
Adds baselines/ingredients found in the literature check (method_design_v1.md):
- FedRS (Li & Zhan, KDD 2021): restricted softmax, missing-class logits scaled by 0.5 during local training.
- GB: class-balanced loss with GLOBAL class counts (shared aggregate statistics; Ratio-loss / BalanceFL family).
- GB+CR: plus class-row head aggregation (row c averaged only over clients holding c, weighted by their count).
- GB+CR+OW: plus encoder aggregation weights proportional to each client's balanced effective mass sum_c n_ic w_c.
References re-run with the same seeds: FedAvg-bal, CCVR, Central-bal.
Usage: python3 pilot3_fl.py --seeds 3 --out ../results/pilot3.csv
"""
from __future__ import annotations

import argparse
import os
import time

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, matthews_corrcoef

from pilot_fl import CLASSES, N_BENIGN_TEST, RARE, ROUNDS, avg, init, load, local_train, make_clients, predict
from pilot2_fl import ccvr, class_weights


def run(X, y, part, seed, alpha, k, log, methods=None):
    rng = np.random.default_rng(seed * 1000 + int(alpha * 100) + k)
    C = len(CLASSES); d = X.shape[1]
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    clients, owner = make_clients(Z, y, part, rng, alpha, k, 1.0)  # identical draws to pilots 1 and 2
    te = np.where(part == "test")[0]
    ben_te = rng.choice(te[y[te] == 0], N_BENIGN_TEST, replace=False)
    te = np.concatenate([ben_te, te[y[te] != 0]]); Xte, yte = Z[te], y[te]
    p0 = init(d, C, rng)
    n = np.stack([np.bincount(y[idx], minlength=C) for idx in clients]).astype(float)   # clients x classes
    Nc = n.sum(0); wg = np.where(Nc > 0, 1 / np.sqrt(np.maximum(Nc, 1)), 0)
    wg = (wg / (wg @ Nc / Nc.sum())).astype(np.float32)                                  # mean weight 1 over all samples
    CWl = [class_weights(y[idx], C) for idx in clients]
    LS = [np.where(n[j] > 0, 1.0, 0.5).astype(np.float32) for j in range(len(clients))]
    sizes = n.sum(1); mass = n @ wg
    out = {}

    def fl(cw_global=False, local_bal=False, rs=False, rows=False, ow=False):
        p = p0
        for _ in range(ROUNDS):
            ups = [local_train(p, Z[idx], y[idx], rng, cw=wg if cw_global else (CWl[j] if local_bal else None),
                               lscale=LS[j] if rs else None) for j, idx in enumerate(clients)]
            p = avg(ups, mass if ow else sizes)
            if rows:  # class-row aggregation of the head
                for c in range(C):
                    h = n[:, c] > 0
                    if h.any():
                        w = n[h, c] / n[h, c].sum()
                        p["Wh"][:, c] = sum(wi * ups[j]["Wh"][:, c] for wi, j in zip(w, np.where(h)[0]))
                        p["bh"][c] = sum(wi * ups[j]["bh"][c] for wi, j in zip(w, np.where(h)[0]))
        return p

    for name, kw in [("FedAvg-bal", {"local_bal": True}), ("FedRS", {"rs": True}), ("GB", {"cw_global": True}),
                     ("GB+CR", {"cw_global": True, "rows": True}), ("GB+CR+OW", {"cw_global": True, "rows": True, "ow": True})]:
        if methods is not None and name not in methods:
            continue
        t0 = time.time(); p = fl(**kw); out[name] = predict(p, Xte)
        if name == "FedAvg-bal":
            out["CCVR"] = predict(ccvr(p, Z, y, clients, C, rng), Xte)
        log(f"  {name} {time.time() - t0:.0f}s")
    allidx = np.concatenate(clients)
    out["Central-bal"] = predict(local_train(p0, Z[allidx], y[allidx], rng, epochs=ROUNDS, cw=class_weights(y[allidx], C)), Xte)
    rows = []
    for meth, pred in out.items():
        for c in CLASSES:
            ci = CLASSES.index(c); m = yte == ci; tp = ((pred == ci) & m).sum(); fp = ((pred == ci) & ~m).sum()
            rec, prec = tp / max(m.sum(), 1), tp / max(tp + fp, 1)
            rows.append(dict(seed=seed, alpha=alpha, k=k, method=meth, cls=c, rare=c in RARE, recall=rec, precision=prec,
                             f1=0.0 if rec + prec == 0 else 2 * rec * prec / (rec + prec)))
        rows.append(dict(seed=seed, alpha=alpha, k=k, method=meth, cls="_overall", rare=False,
                         f1=f1_score(yte, pred, average="macro"), mcc=matthews_corrcoef(yte, pred)))
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)
    X, y, part, _ = load(); log(f"loaded {X.shape}")
    rows, done = [], set()
    if os.path.exists(a.out):
        prev = pd.read_csv(a.out); rows = prev.to_dict("records")
        done = set(map(tuple, prev[["seed", "alpha", "k"]].drop_duplicates().to_numpy().tolist()))
    for seed in range(a.seeds):
        for alpha in (0.1, 0.5):
            for k in (5, 20, 100):
                if (seed, alpha, k) in done:
                    continue
                log(f"seed={seed} alpha={alpha} k={k}")
                rows += run(X, y, part, seed, alpha, k, log)
                pd.DataFrame(rows).to_csv(a.out, index=False)
    log("finished")

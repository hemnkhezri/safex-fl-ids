"""Pilot 2 (development, not sealed): do known fixes for label-skew classifier bias close the gap on
client-exclusive rare attack classes? Design: pilot_verdict_v1.md "Next step"; same data, splits, clients and
encoder as pilot_fl.py.

Global view (one model used by every client): FedAvg, FedAvg-bal (class-balanced CE), FedLC (logit adjustment
by the local label prior, balanced-softmax form), CCVR (classifier re-trained on virtual features sampled from
federated class means/covariances, on top of FedAvg-bal), Proto-count-bal.
Owner view (the rare class owner's own model): Local-owner-bal, FedRep (shared body, personal head).
References: Central-head, Central-bal, Central-proto (pooled data, same epochs).
Usage: python3 pilot2_fl.py --frac 1.0 --seeds 5 --out ../results/pilot2_full.csv
"""
from __future__ import annotations

import argparse
import os
import time

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, matthews_corrcoef

from pilot_fl import (CLASSES, EMB, K_CLIENTS, N_BENIGN_TEST, RARE, ROUNDS, aggregate_protos, avg, embed, init,
                      load, local_stats, local_train, make_clients, predict)

BODY = ("W1", "b1", "W2", "b2"); HEAD = ("Wh", "bh")
N_VIRTUAL, SHRINK = 2000, 10.0


def class_weights(y, C):
    n = np.bincount(y, minlength=C).astype(float)
    w = np.where(n > 0, 1 / np.sqrt(np.maximum(n, 1)), 0.0)
    return (w / (w[y].mean())).astype(np.float32)


def prior_adj(y, C):
    n = np.bincount(y, minlength=C).astype(float)
    return np.log(np.maximum(n / n.sum(), 1e-6)).astype(np.float32)


def ccvr(p, Z, y, clients, C, rng):
    """Classifier calibration with virtual representations (Luo et al., NeurIPS 2021), Gaussian per class."""
    S1 = np.zeros((C, EMB)); S2 = np.zeros((C, EMB, EMB)); N = np.zeros(C)
    for idx in clients:  # each client sends per-class n, sum, sum of outer products of embeddings
        h = embed(p, Z[idx]).astype(float); yy = y[idx]
        for c in np.unique(yy):
            hc = h[yy == c]; N[c] += len(hc); S1[c] += hc.sum(0); S2[c] += hc.T @ hc
    present = np.where(N > 0)[0]
    mu = S1[present] / N[present, None]
    cov = S2[present] / N[present, None, None] - np.einsum("ci,cj->cij", mu, mu)
    avg_var = np.mean([np.trace(c) / EMB for c in cov])
    feats, labs = [], []
    for j, c in enumerate(present):
        lam = N[c] / (N[c] + SHRINK)
        cc = lam * cov[j] + (1 - lam) * avg_var * np.eye(EMB) + 1e-6 * np.eye(EMB)
        feats.append(rng.multivariate_normal(mu[j], cc, N_VIRTUAL)); labs.append(np.full(N_VIRTUAL, c))
    H = np.vstack(feats).astype(np.float32); L = np.concatenate(labs)
    Wh, bh = p["Wh"].copy(), p["bh"].copy()
    for _ in range(300):  # full-batch gradient descent on the head
        lo = H @ Wh + bh; lo -= lo.max(1, keepdims=True); pr = np.exp(lo); pr /= pr.sum(1, keepdims=True)
        pr[np.arange(len(L)), L] -= 1; pr /= len(L)
        Wh -= 0.5 * (H.T @ pr); bh -= 0.5 * pr.sum(0)
    q = dict(p); q["Wh"], q["bh"] = Wh, bh
    return q


def run(X, y, part, seed, alpha, k, frac, log):
    rng = np.random.default_rng(seed * 1000 + int(alpha * 100) + k)
    C = len(CLASSES); d = X.shape[1]
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    clients, owner = make_clients(Z, y, part, rng, alpha, k, frac)  # same rng sequence as pilot 1
    te = np.where(part == "test")[0]
    ben_te = te[y[te] == 0]; ben_te = rng.choice(ben_te, min(len(ben_te), int(N_BENIGN_TEST * max(frac, 0.2))), replace=False)
    te = np.concatenate([ben_te, te[y[te] != 0]]); Xte, yte = Z[te], y[te]
    p0 = init(d, C, rng)
    CW = [class_weights(y[idx], C) for idx in clients]; LA = [prior_adj(y[idx], C) for idx in clients]
    sizes = np.array([len(i) for i in clients], float)
    out, own = {}, {}

    def fl(bal=False, lc=False, proto=False):
        p, G = p0, None
        for _ in range(ROUNDS):
            ups = [local_train(p, Z[idx], y[idx], rng, protos=G, cw=CW[j] if bal else None, ladj=LA[j] if lc else None)
                   for j, idx in enumerate(clients)]
            if proto:
                G, _ = aggregate_protos([local_stats(u, Z[idx], y[idx], C) for u, idx in zip(ups, clients)], "count", C)
            p = avg(ups, sizes)
        return p, G

    for name, kw in [("FedAvg", {}), ("FedAvg-bal", {"bal": True}), ("FedLC", {"lc": True}),
                     ("Proto-count-bal", {"bal": True, "proto": True})]:
        t0 = time.time(); p, G = fl(**kw); out[name] = predict(p, Xte, G)
        if name == "FedAvg-bal":
            out["CCVR"] = predict(ccvr(p, Z, y, clients, C, rng), Xte)
        log(f"  {name} {time.time() - t0:.0f}s")
    # FedRep: body averaged, heads stay local
    t0 = time.time(); body = {k_: v for k_, v in p0.items()}; heads = [{h: p0[h].copy() for h in HEAD} for _ in clients]
    for _ in range(ROUNDS):
        ups = []
        for j, idx in enumerate(clients):
            pj = {**body, **heads[j]}
            pj = local_train(pj, Z[idx], y[idx], rng, cw=CW[j], train=HEAD)       # head first (body frozen)
            pj = local_train(pj, Z[idx], y[idx], rng, cw=CW[j], train=BODY)       # then body (head frozen)
            heads[j] = {h: pj[h] for h in HEAD}; ups.append(pj)
        body = avg(ups, sizes)
    for c, j in owner.items():
        own[("FedRep", c)] = predict({**body, **heads[j]}, Xte)
    log(f"  FedRep {time.time() - t0:.0f}s")
    allidx = np.concatenate(clients); t0 = time.time()
    pc = local_train(p0, Z[allidx], y[allidx], rng, epochs=ROUNDS); out["Central-head"] = predict(pc, Xte)
    out["Central-proto"] = predict(pc, Xte, local_stats(pc, Z[allidx], y[allidx], C)[0])
    pcb = local_train(p0, Z[allidx], y[allidx], rng, epochs=ROUNDS, cw=class_weights(y[allidx], C))
    out["Central-bal"] = predict(pcb, Xte)
    log(f"  Central {time.time() - t0:.0f}s")
    for c, j in owner.items():
        idx = clients[j]
        own[("Local-owner-bal", c)] = predict(local_train(p0, Z[idx], y[idx], rng, epochs=ROUNDS, cw=CW[j]), Xte)
    rows = []

    def score(meth, pred, classes, view):
        for c in classes:
            ci = CLASSES.index(c); m = yte == ci; tp = ((pred == ci) & m).sum(); fp = ((pred == ci) & ~m).sum()
            rec, prec = tp / max(m.sum(), 1), tp / max(tp + fp, 1)
            rows.append(dict(seed=seed, alpha=alpha, k=k, method=meth, view=view, cls=c, rare=c in RARE,
                             n_test=int(m.sum()), recall=rec, precision=prec,
                             f1=0.0 if rec + prec == 0 else 2 * rec * prec / (rec + prec)))
    for meth, pred in out.items():
        score(meth, pred, CLASSES, "global")
        rows.append(dict(seed=seed, alpha=alpha, k=k, method=meth, view="global", cls="_overall", rare=False,
                         n_test=len(yte), recall=np.nan, precision=np.nan,
                         f1=f1_score(yte, pred, average="macro"), mcc=matthews_corrcoef(yte, pred)))
    for (meth, c), pred in own.items():
        score(meth, pred, [c], "owner")
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frac", type=float, default=1.0); ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--alphas", default="0.1,0.5"); ap.add_argument("--ks", default="5,20,100")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)
    X, y, part, n_dup = load(); log(f"loaded {X.shape}, removed {n_dup} duplicated test rows")
    rows, done = [], set()
    if os.path.exists(a.out):  # resume after an interruption: keep finished settings
        prev = pd.read_csv(a.out); rows = prev.to_dict("records")
        done = set(map(tuple, prev[["seed", "alpha", "k"]].drop_duplicates().to_numpy().tolist()))
        log(f"resuming, {len(done)} settings already done")
    for seed in range(a.seeds):
        for alpha in map(float, a.alphas.split(",")):
            for k in map(int, a.ks.split(",")):
                if (seed, alpha, k) in done:
                    continue
                log(f"seed={seed} alpha={alpha} k={k}")
                rows += run(X, y, part, seed, alpha, k, a.frac, log)
                os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
                pd.DataFrame(rows).to_csv(a.out, index=False)
    log("done")

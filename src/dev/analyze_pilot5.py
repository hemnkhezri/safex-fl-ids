"""Analyse pilot 5: shared owner experts + calibration variants vs federated baselines (+OC) and the owner alone.
Usage: python3 analyze_pilot5.py ../results/pilot5 [../results/pilot6] > report.md
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

Q = 1e-3


def margin(L, c):
    o = L.copy(); o[:, c] = -np.inf
    return L[:, c] - o.max(1)


def prf(m, pr):
    tp = (pr & m).sum(); p = tp / max(pr.sum(), 1); r = tp / max(m.sum(), 1)
    return p, r, (0 if p + r == 0 else 2 * p * r / (p + r))


def fuse(G, scores, taus, rid, nrid):
    pred = np.array(nrid)[G[:, nrid].argmax(1)]
    ex = np.stack([s - t for s, t in zip(scores, taus)], 1); hit = ex.max(1) >= 0
    pred[hit] = np.array(rid)[ex[hit].argmax(1)]
    return pred


rows = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.npz"))):
    ds, seed, k = re.match(r"(\w+)_s(\d+)_k(\d+)\.npz", os.path.basename(f)).groups()
    z = np.load(f); cls = list(z["classes"]); rare = list(z["rare"]); y = z["y_test"]
    rid = [cls.index(c) for c in rare]; nrid = [i for i in range(len(cls)) if i not in rid]
    meta = dict(ds=ds, seed=int(seed), k=int(k)); own = z["owner"]; ns = z["neg_sizes"]; cut = np.cumsum(ns)[:-1]

    def score(pred, method, view="global"):
        for ci, c in enumerate(cls):
            p, r, f1 = prf(y == ci, pred == ci)
            rows.append(dict(meta, method=method, view=view, cls=c,
                             group="rare" if c in rare else ("benign" if ci == 0 else "common"), precision=p, recall=r, f1=f1))
    for m in ("CCVR", "FedProx-bal", "GB+CR", "Central-bal"):
        L = z[f"{m}|test"]; score(L.argmax(1), f"{m} argmax")
        tv = [np.quantile(margin(z[f"{m}|cal"], c), 1 - Q) for c in rid]
        score(fuse(L, [margin(L, c) for c in rid], tv, rid, nrid), f"{m}+OC")
    f6 = os.path.join(sys.argv[2], os.path.basename(f)) if len(sys.argv) > 2 else ""
    if f6 and os.path.exists(f6):  # mandatory baselines from pilot 6 (same test set)
        z6 = np.load(f6); assert (z6["y_test"] == y).all()
        for m in ("PROTEAN", "FedOV"):
            L = z6[f"{m}|test"]; score(L.argmax(1), f"{m} argmax")
            tv = [np.quantile(margin(z6[f"{m}|cal"], c), 1 - Q) for c in rid]
            score(fuse(L, [margin(L, c) for c in rid], tv, rid, nrid), f"{m}+OC")
    S = [margin(z[f"expert_{c}|test"], ci) for c, ci in zip(rare, rid)]
    for i, (c, ci) in enumerate(zip(rare, rid)):  # owner alone, on its own class
        p, r, f1 = prf(y == ci, z[f"expert_{c}|test"].argmax(1) == ci)
        rows.append(dict(meta, method="Owner alone", view="owner", cls=c, group="rare", precision=p, recall=r, f1=f1))
    taus = {"none (argmax)": [0.0] * len(rid)}
    for i, (c, ci) in enumerate(zip(rare, rid)):
        sa = margin(z[f"expert_{c}|negall"], ci); parts = np.split(sa, cut)
        taus.setdefault("own", []).append(np.quantile(parts[own[i]], 1 - Q))
        taus.setdefault("fed", []).append(np.quantile(sa, 1 - Q))
        taus.setdefault("fed-others", []).append(np.quantile(np.concatenate([p_ for j, p_ in enumerate(parts) if j != own[i]]), 1 - Q))
        taus.setdefault("val", []).append(np.quantile(margin(z[f"expert_{c}|cal"], ci), 1 - Q))
    for base in ("GB+CR", "FedProx-bal"):
        G = z[f"{base}|test"]
        for name, t in taus.items():
            score(fuse(G, S, t, rid, nrid), f"Experts[{name}] + {base}")
d = pd.DataFrame(rows)
print("# Pilot 5: shared owner experts (development seeds 0-4, alpha=0.5)\n")
g = d[d.view == "global"]
t = g.groupby(["ds", "k", "seed", "method", "group"]).f1.mean().unstack("group").groupby(["ds", "k", "method"]).mean()
pr = g[g.group == "rare"].groupby(["ds", "k", "method"])[["precision", "recall"]].mean()
br = g[g.group == "benign"].groupby(["ds", "k", "method"]).recall.mean().rename("benign_recall")
t = t.join(pr).join(br)[["rare", "precision", "recall", "common", "benign_recall"]].round(3)
for (ds, k), sub in t.groupby(level=["ds", "k"]):
    print(f"## {ds}, k={k}\n"); print(sub.droplevel([0, 1]).sort_values("rare", ascending=False).to_markdown(), "\n")
o = d[d.view == "owner"].groupby(["ds", "k"]).f1.mean().round(3)
print("## Owner alone (on its own class)\n"); print(o.to_markdown(), "\n")
rng = np.random.default_rng(0)
print("## Paired rare-F1 differences (x100), 95% CI over seeds\n")
r = g[g.group == "rare"].groupby(["ds", "k", "seed", "method"]).f1.mean().unstack("method")
for (ds, k), sub in r.groupby(level=["ds", "k"]):
    base_cols = [c for c in sub.columns if (c.endswith("+OC") or c.endswith("argmax")) and not c.startswith("Central")]
    best_base = sub[base_cols].max(axis=1)  # best baseline per seed, argmax or +OC (conservative)
    for new in ("Experts[fed] + GB+CR", "Experts[fed-others] + GB+CR", "Experts[fed] + FedProx-bal"):
        dd = (sub[new] - best_base).to_numpy(); bs = rng.choice(dd, (4000, len(dd))).mean(1)
        print(f"- {ds} k={k}: {new} - best baseline: {100 * dd.mean():+.1f} [{100 * np.percentile(bs, 2.5):+.1f}, {100 * np.percentile(bs, 97.5):+.1f}]")
    dd = (sub["Central-bal argmax"] - sub["Experts[fed] + GB+CR"]).to_numpy()
    print(f"- {ds} k={k}: Central-bal - Experts[fed]+GB+CR: {100 * dd.mean():+.1f}")

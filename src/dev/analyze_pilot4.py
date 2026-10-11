"""Analyse pilot 4: owner-calibrated rare-class decision (step 4) on saved logits.
Rule OC(q, source): for each rare class c, margin s_c = logit_c - max_{j != c} logit_j. Its owner sets
tau_c = (1 - q) quantile of s_c on calibration negatives (no rare flows): 'val' = validation-period sample
(held-out traffic), 'own' = owner's own non-rare training flows (in-sample, naive). Prediction: if some rare c has
s_c >= tau_c, predict the one with the largest s_c - tau_c; otherwise argmax over the non-rare classes.
'oracle' = per-class threshold maximising test F1 (upper bound on what any threshold can do; not a method).
Usage: python3 analyze_pilot4.py ../results/pilot4 > ../results/pilot4_report.md
"""
import glob
import re
import sys

import numpy as np
import pandas as pd

from pilot_fl import CLASSES, RARE

RID = [CLASSES.index(c) for c in RARE]; NRID = [i for i in range(len(CLASSES)) if i not in RID]
QS = (1e-4, 1e-3, 1e-2)


def margin(L, c):
    o = L.copy(); o[:, c] = -np.inf
    return L[:, c] - o.max(1)


def decide(L, taus):
    pred = np.array(NRID)[L[:, NRID].argmax(1)]
    ex = np.stack([margin(L, c) - taus[i] for i, c in enumerate(RID)], 1)
    hit = ex.max(1) >= 0
    pred[hit] = np.array(RID)[ex[hit].argmax(1)]
    return pred


def oracle_taus(L, y):
    taus = []
    for c in RID:
        s = margin(L, c); pos = y == c
        cand = np.unique(np.quantile(s[pos], np.linspace(0, 1, 41))) if pos.any() else [np.inf]
        best = max(cand, key=lambda t: f1(pos, s >= t))
        taus.append(best if f1(pos, s >= best) > 0 else np.inf)  # never fire a class no threshold can detect
    return np.array(taus)


def f1(m, pr):
    tp = (pr & m).sum(); p = tp / max(pr.sum(), 1); r = tp / max(m.sum(), 1)
    return 0 if p + r == 0 else 2 * p * r / (p + r)


def score(pred, y, **meta):
    rows = []
    for ci, c in enumerate(CLASSES):
        m = y == ci; pr = pred == ci; tp = (pr & m).sum()
        prec, rec = tp / max(pr.sum(), 1), tp / max(m.sum(), 1)
        rows.append(dict(meta, cls=c, rare=c in RARE, precision=prec, recall=rec,
                         f1=0 if prec + rec == 0 else 2 * prec * rec / (prec + rec)))
    return rows


rows = []
for f in sorted(glob.glob(f"{sys.argv[1]}/seed*_k*.npz")):
    seed, k = map(int, re.findall(r"seed(\d+)_k(\d+)", f)[0]); z = np.load(f); yt = z["y_test"]
    for m in ("FedAvg-bal", "CCVR", "GB+CR", "Central-bal"):
        L = z[f"{m}|test"]; meta = dict(seed=seed, k=k, model=m)
        rows += score(L.argmax(1), yt, **meta, rule="argmax")
        for q in QS:
            tv = np.array([np.quantile(margin(z[f"{m}|cal"], c), 1 - q) for c in RID])
            to = np.array([np.quantile(margin(z[f"{m}|own_{CLASSES[c]}"], c), 1 - q) for c in RID])
            rows += score(decide(L, tv), yt, **meta, rule=f"OC-val q={q:g}")
            rows += score(decide(L, to), yt, **meta, rule=f"OC-own q={q:g}")
        rows += score(decide(L, oracle_taus(L, yt)), yt, **meta, rule="oracle")
d = pd.DataFrame(rows); r = d[d.rare]
rng = np.random.default_rng(0)


def boot(g, col):
    s = g.seed.unique(); e = g.groupby("seed")[col].mean().mean()
    bs = [g[g.seed.isin(rng.choice(s, len(s)))].groupby("seed")[col].mean().mean() for _ in range(4000)]
    return 100 * e, 100 * np.percentile(bs, [2.5, 97.5])


print(f"# Pilot 4: owner-calibrated rare-class threshold (step 4), alpha=0.5, E=5, R=60, seeds {sorted(d.seed.unique())}\n")
for k, g in r.groupby("k"):
    print(f"## k={k}: rare-class F1 / precision / recall (mean over 4 rare classes and seeds)\n")
    t = g.groupby(["rule", "model"])[["f1", "precision", "recall"]].mean().unstack().round(3)
    print(t.to_markdown(), "\n")
c = d[(~d.rare) & (d.cls != "Benign")].groupby(["k", "rule", "model"]).f1.mean().unstack().round(3)
print("## Common attack classes F1\n"); print(c.to_markdown(), "\n")
b = d[d.cls == "Benign"].groupby(["k", "rule", "model"]).recall.mean().unstack().round(4)
print("## Benign recall\n"); print(b.to_markdown(), "\n")
p = r.pivot_table(index=["seed", "k", "cls"], columns=["model", "rule"], values="f1")
print("## Paired rare-class F1 differences (x100), 95% CI bootstrap over seeds\n")
for q in QS:
    rule = f"OC-val q={q:g}"
    for k in sorted(r.k.unique()):
        g = p.xs(k, level="k").reset_index()
        g.columns = ["|".join(x) if x[1] else x[0] for x in g.columns]
        g["a"] = g[f"GB+CR|{rule}"] - g["CCVR|argmax"]
        g["b"] = g[f"GB+CR|{rule}"] - g["GB+CR|argmax"]
        g["c"] = g[f"Central-bal|{rule}"] - g[[f"{m}|{rule}" for m in ("GB+CR", "CCVR", "FedAvg-bal")]].max(axis=1)
        g["e"] = g[f"GB+CR|{rule}"] - g[f"CCVR|{rule}"]
        g["d"] = g["Central-bal|argmax"] - g[[f"{m}|{rule}" for m in ("GB+CR", "CCVR", "FedAvg-bal")]].max(axis=1)
        out = []
        for col, lab in (("a", "GB+CR+OC - CCVR"), ("b", "GB+CR+OC - GB+CR"), ("e", "GB+CR+OC - CCVR+OC"), ("c", "Central+OC - best FL+OC"),
                         ("d", "Central argmax - best FL+OC")):
            e, ci = boot(g, col); out.append(f"{lab} {e:+.1f} [{ci[0]:+.1f}, {ci[1]:+.1f}]")
        print(f"- {rule}, k={k}: " + "; ".join(out))

"""Confirmatory analysis for study_plan_experts_v2_SEALED.md (M1-M5).
Usage: python3 analyze_conf2.py ../results/conf2 > ../results/conf2_report.md
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

Q = 1e-3; ROOT = sys.argv[1]
SAFEX = "SAFE-X (Experts[fed] + GB+CR)"; ABL = "Experts[own] + GB+CR"
BASES = ["GB+CR argmax", "GB+CR+OC", "FedProx-bal argmax", "FedProx-bal+OC", "CCVR argmax", "CCVR+OC",
         "PROTEAN argmax", "PROTEAN+OC", "FedOV argmax", "FedOV+OC"]


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


rows, far = [], []
for f in sorted(glob.glob(os.path.join(ROOT, "p5", "*.npz"))):
    ds, seed, k = re.match(r"(\w+)_s(\d+)_k(\d+)\.npz", os.path.basename(f)).groups()
    f6 = os.path.join(ROOT, "p6", os.path.basename(f))
    if not os.path.exists(f6):
        continue
    z = np.load(f); z6 = np.load(f6); cls = list(z["classes"]); rare = list(z["rare"]); y = z["y_test"]
    assert (z6["y_test"] == y).all()
    rid = [cls.index(c) for c in rare]; nrid = [i for i in range(len(cls)) if i not in rid]
    meta = dict(ds=ds, seed=int(seed), k=int(k)); own = z["owner"]; cut = np.cumsum(z["neg_sizes"])[:-1]

    def score(pred, method, view="global"):
        for ci, c in enumerate(cls):
            p, r, f1 = prf(y == ci, pred == ci)
            rows.append(dict(meta, method=method, view=view, cls=c,
                             group="rare" if c in rare else ("benign" if ci == 0 else "common"), precision=p, recall=r, f1=f1))
    for m, zz in (("CCVR", z), ("FedProx-bal", z), ("GB+CR", z), ("Central-bal", z), ("PROTEAN", z6), ("FedOV", z6)):
        L = zz[f"{m}|test"]; score(L.argmax(1), f"{m} argmax")
        tv = [np.quantile(margin(zz[f"{m}|cal"], c), 1 - Q) for c in rid]
        score(fuse(L, [margin(L, c) for c in rid], tv, rid, nrid), f"{m}+OC")
    S = [margin(z[f"expert_{c}|test"], ci) for c, ci in zip(rare, rid)]
    tf, to = [], []; negte = ~np.isin(y, rid)
    for i, (c, ci) in enumerate(zip(rare, rid)):
        p, r, f1 = prf(y == ci, z[f"expert_{c}|test"].argmax(1) == ci)
        rows.append(dict(meta, method="Owner alone", view="owner", cls=c, group="rare", precision=p, recall=r, f1=f1))
        sa = margin(z[f"expert_{c}|negall"], ci); parts = np.split(sa, cut)
        tf.append(np.quantile(sa, 1 - Q)); to.append(np.quantile(parts[own[i]], 1 - Q))
        far.append(dict(meta, cls=c, fed=(S[i][negte] >= tf[-1]).mean(), own=(S[i][negte] >= to[-1]).mean()))
    G = z["GB+CR|test"]
    score(fuse(G, S, tf, rid, nrid), SAFEX); score(fuse(G, S, to, rid, nrid), ABL)
d = pd.DataFrame(rows); fa = pd.DataFrame(far)
d.to_csv(os.path.join(ROOT, "..", "conf2_scores.csv"), index=False)
rng = np.random.default_rng(0)


def boot(v):
    v = np.asarray(v); bs = rng.choice(v, (4000, len(v))).mean(1)
    return v.mean(), np.percentile(bs, [2.5, 97.5])


def fmt(e, ci, s=100):
    return f"{s * e:+.1f} [{s * ci[0]:+.1f}, {s * ci[1]:+.1f}]"


g = d[d.view == "global"]
F = g.groupby(["ds", "k", "seed", "method", "group"]).f1.mean().unstack("group")
print("# Confirmatory results, plan v2 (SAFE-X)\n")
print("Units per (ds, k):", F.reset_index().groupby(["ds", "k"]).seed.nunique().to_dict(), "\n")
tab = F.rare.groupby(["ds", "k", "method"]).mean().unstack("k").round(3)
print("## Rare-class F1 (seed means)\n"); print(tab.to_markdown(), "\n")
own_v = d[d.view == "owner"].groupby(["ds", "k"]).f1.mean().round(3)
print("Owner alone (own class):", own_v.to_dict(), "\n")
print("## M1: SAFE-X - FedOV+OC (rare F1 x100, pooled over k)\n")
m1 = {}
for ds, sub in F.rare.groupby(level="ds"):
    r = sub.unstack("method"); diff = (r[SAFEX] - r["FedOV+OC"]).groupby(level="seed").mean()
    e, ci = boot(diff); m1[ds] = ci[0] > 0
    print(f"- {ds}: {fmt(e, ci)} -> {'SUPPORTED' if m1[ds] else 'NOT supported'}")
print(f"\n**M1 main claim (both datasets): {'SUPPORTED' if all(m1.values()) else 'NOT supported'}**\n")
print("## M2: SAFE-X - best baseline per (dataset, k)\n")
for (ds, k), sub in F.rare.groupby(level=["ds", "k"]):
    r = sub.unstack("method"); best = r[BASES].mean().idxmax()
    e, ci = boot(r[SAFEX] - r[best])
    print(f"- {ds} k={k}: best baseline {best} ({r[best].mean():.3f}); SAFE-X {r[SAFEX].mean():.3f}; diff {fmt(e, ci)}{' (claimed)' if ci[0] > 0 else ''}")
print("\n## M3: false-alarm rate of shared experts on non-rare test flows (target 0.001)\n")
for ds, sub in fa.groupby("ds"):
    ps = sub.groupby("seed")[["fed", "own"]].mean(); e, ci = boot(ps.own - ps.fed)
    print(f"- {ds}: owner-only {sub.own.mean():.4f} (worst {sub.own.max():.4f}); federated {sub.fed.mean():.4f} "
          f"(worst {sub.fed.max():.4f}); owner-only - federated {fmt(e, ci, 1000)} per mille -> {'SUPPORTED' if ci[0] > 0 else 'NOT supported'}")
print("\n## M4: no harm vs GB+CR argmax (benign recall >= -0.002, common F1 >= -1 pt)\n")
br = g[g.group == "benign"].groupby(["ds", "k", "method"]).recall.mean()
cf = F.common.groupby(["ds", "k", "method"]).mean()
for (ds, k) in sorted({(a, b) for a, b, _ in br.index}):
    db = br[(ds, k, SAFEX)] - br[(ds, k, "GB+CR argmax")]; dc = 100 * (cf[(ds, k, SAFEX)] - cf[(ds, k, "GB+CR argmax")])
    print(f"- {ds} k={k}: benign recall {db:+.4f}; common F1 {dc:+.2f} pts -> {'pass' if db >= -0.002 and dc >= -1 else 'FAIL'}")
print("\n## M5 (descriptive): SAFE-X vs Owner alone and Central-bal (rare F1)\n")
for (ds, k), sub in F.rare.groupby(level=["ds", "k"]):
    r = sub.unstack("method")
    print(f"- {ds} k={k}: SAFE-X {r[SAFEX].mean():.3f}; owner alone {own_v[(ds, k)]:.3f}; Central-bal {r['Central-bal argmax'].mean():.3f}; "
          f"ablation owner-only calibration {r[ABL].mean():.3f}")

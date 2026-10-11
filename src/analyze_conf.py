"""Confirmatory analysis: applies the sealed decision rules of study_plan_hybrid_v1_SEALED.md (section 2) to the
saved logits in results/conf/. OC = owner-calibrated threshold (see analyze_pilot4.py).
Usage: python3 analyze_conf.py ../results/conf > ../results/conf_report.md
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

GLOBAL_FL = ["FedAvg", "FedAvg-bal", "FedProx-bal", "FedLC", "FedRS", "CCVR", "GB+CR"]
OC_SET = ["FedAvg-bal", "FedProx-bal", "FedLC", "FedRS", "CCVR", "GB+CR"]
Q = 1e-3


def margin(L, c):
    o = L.copy(); o[:, c] = -np.inf
    return L[:, c] - o.max(1)


def decide(L, taus, rid, nrid):
    pred = np.array(nrid)[L[:, nrid].argmax(1)]
    ex = np.stack([margin(L, c) - taus[i] for i, c in enumerate(rid)], 1)
    hit = ex.max(1) >= 0
    pred[hit] = np.array(rid)[ex[hit].argmax(1)]
    return pred


def prf(m, pr):
    tp = (pr & m).sum(); p = tp / max(pr.sum(), 1); r = tp / max(m.sum(), 1)
    return p, r, (0 if p + r == 0 else 2 * p * r / (p + r))


rows = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.npz"))):
    ds, arm, seed, alpha, k = re.match(r"(\w+)_(\w+)_s(\d+)_a([\d.]+)_k(\d+)\.npz", os.path.basename(f)).groups()
    z = np.load(f); cls = list(z["classes"]); rare = list(z["rare"]); y = z["y_test"]
    rid = [cls.index(c) for c in rare]; nrid = [i for i in range(len(cls)) if i not in rid]
    meta = dict(ds=ds, arm=arm, seed=int(seed), alpha=float(alpha), k=int(k))
    models = sorted({key.split("|")[0] for key in z.keys() if key.endswith("|test") and "owner_" not in key})

    def score(pred, model, rule):
        for ci, c in enumerate(cls):
            p, r, f1 = prf(y == ci, pred == ci)
            rows.append(dict(meta, model=model, rule=rule, view="global", cls=c,
                             group="rare" if c in rare else ("benign" if ci == 0 else "common"),
                             precision=p, recall=r, f1=f1))
    for m in models:
        L = z[f"{m}|test"]
        score(L.argmax(1), m, "argmax")
        for q in (1e-4, 1e-3, 1e-2):
            tv = np.array([np.quantile(margin(z[f"{m}|cal"], c), 1 - q) for c in rid])
            score(decide(L, tv, rid, nrid), m, f"OC q={q:g}")
        to = np.array([np.quantile(margin(z[f"{m}|own_{cls[c]}"], c), 1 - Q) for c in rid])
        score(decide(L, to, rid, nrid), m, "OC-own q=0.001")
    for key in z.keys():
        mm = re.match(r"(.+)\|owner_(.+)\|test", key)
        if mm:
            c = mm.group(2); p, r, f1 = prf(y == cls.index(c), z[key].argmax(1) == cls.index(c))
            rows.append(dict(meta, model=mm.group(1), rule="argmax", view="owner", cls=c, group="rare",
                             precision=p, recall=r, f1=f1))
d = pd.DataFrame(rows)
d.to_csv(os.path.join(sys.argv[1], "..", "conf_scores.csv"), index=False)
rng = np.random.default_rng(0)


def boot(s):
    """s: per-seed values (Series indexed by seed) -> mean, CI."""
    v = s.to_numpy(); bs = rng.choice(v, (4000, len(v))).mean(1)
    return 100 * v.mean(), 100 * np.percentile(bs, [2.5, 97.5])


def fmt(e, ci):
    return f"{e:+.1f} [{ci[0]:+.1f}, {ci[1]:+.1f}]"


g = d[d.view == "global"]
gm = g.groupby(["ds", "arm", "alpha", "k", "seed", "model", "rule", "group"]).f1.mean().unstack("group")
print("# Confirmatory results (sealed plan v1)\n")
print("Units:", d.groupby(["ds", "arm", "alpha", "k"]).seed.nunique().to_dict(), "\n")
for (ds, arm, a), sub in gm.groupby(level=["ds", "arm", "alpha"]):
    print(f"## {ds}, arm={arm}, alpha={a}: rare-class F1 (seed mean)\n")
    t = sub.rare.groupby(level=["k", "model", "rule"]).mean().unstack("k").round(3)
    print(t.to_markdown(), "\n")
rare_pr = g[g.group == "rare"].groupby(["ds", "arm", "alpha", "k", "model", "rule"])[["precision", "recall"]].mean()

P = d[(d.arm == "primary") & (d.alpha == 0.5)]
R = P[(P.view == "global")].groupby(["ds", "k", "seed", "model", "rule", "group"]).f1.mean().unstack("group")
print("## H1 gap: Central-bal argmax - best global FL argmax (rare F1 x100)\n")
h1 = {}
for (ds, k), sub in R.groupby(level=["ds", "k"]):
    r = sub.rare.unstack(["model", "rule"])
    gap = r[("Central-bal", "argmax")] - r[[(m, "argmax") for m in GLOBAL_FL]].max(axis=1)
    e, ci = boot(gap); h1[(ds, k)] = ci[0] > 0
    print(f"- {ds} k={k}: {fmt(e, ci)}")
for ds in P.ds.unique():
    print(f"\n**H1 {ds}: {'SUPPORTED' if sum(h1[(ds, k)] for k in (5, 20, 100) if (ds, k) in h1) >= 2 else 'NOT supported'}**")

print("\n## H3 failure split (rare precision / recall, seed means)\n")
h3 = True
for (ds, k), _ in R.groupby(level=["ds", "k"]):
    c = rare_pr.loc[(ds, "primary", 0.5, k, "CCVR", "argmax")]; gb = rare_pr.loc[(ds, "primary", 0.5, k, "GB+CR", "argmax")]
    ok = c.recall > gb.recall and gb.precision > c.precision; h3 &= ok
    print(f"- {ds} k={k}: CCVR P {c.precision:.3f} R {c.recall:.3f}; GB+CR P {gb.precision:.3f} R {gb.recall:.3f} -> {'yes' if ok else 'no'}")
print(f"\n**H3: {'SUPPORTED' if h3 else 'NOT supported'}**")

print("\n## H4 OC vs argmax per model (rare F1 x100, pooled over k; harm checks)\n")
rule = "OC q=0.001"
for ds in P.ds.unique():
    sub = R.xs(ds, level="ds"); wins = 0
    for m in OC_SET:
        a = sub.xs((m, "argmax"), level=["model", "rule"]); o = sub.xs((m, rule), level=["model", "rule"])
        diff = (o.rare - a.rare).groupby(level="seed").mean(); e, ci = boot(diff)
        dc = 100 * (o.common - a.common).mean(); db = (o.benign - a.benign).mean()
        bn = g[(g.ds == ds) & (g.arm == "primary") & (g.alpha == 0.5) & (g.model == m) & (g.group == "benign")]
        brec = bn.groupby("rule").recall.mean(); dbr = brec[rule] - brec["argmax"]
        ok = ci[0] > 0 and dc >= -1 and dbr >= -0.002; wins += ok
        print(f"- {ds} {m}: {fmt(e, ci)}; common F1 {dc:+.2f} pts; benign recall {dbr:+.4f} -> {'pass' if ok else 'fail'}")
    print(f"\n**H4 {ds}: {wins}/6 models pass -> {'SUPPORTED' if wins >= 4 else 'NOT supported'}**\n")

print("## P (primary claim): best fixed FL+OC model - best FL argmax per setting (rare F1 x100)\n")
mean_oc = {m: R.xs((m, rule), level=["model", "rule"]).rare.mean() for m in OC_SET}
best = max(mean_oc, key=mean_oc.get); print(f"best fixed FL+OC model: {best} (mean rare F1 {mean_oc[best]:.3f})\n")
allok = True
for (ds, k), sub in R.groupby(level=["ds", "k"]):
    r = sub.rare.unstack(["model", "rule"])
    bfl = r[[(m, "argmax") for m in GLOBAL_FL]].max(axis=1)
    e, ci = boot(r[(best, rule)] - bfl); allok &= ci[0] > 0
    g1, _ = boot(r[("Central-bal", "argmax")] - bfl); g2, ci5 = boot(r[("Central-bal", "argmax")] - r[(best, rule)])
    print(f"- {ds} k={k}: {fmt(e, ci)}; gap closed {100 * (1 - g2 / g1):.0f}%; H5 residual {fmt(g2, ci5)}")
print(f"\n**P: {'SUPPORTED' if allok else 'NOT supported'}**\n")

E = d[(d.arm.isin(["e1"])) | ((d.arm == "primary") & (d.alpha == 0.5) & (d.k == 20) & (d.seed < 105))]
E = E[E.view == "global"].groupby(["ds", "arm", "seed", "model", "rule", "group"]).f1.mean().unstack("group").common
print("## H2 under-training confound: (Central - FedAvg-bal) common F1 gap at E=1 minus at E=5 (x100)\n")
for ds in E.index.get_level_values("ds").unique():
    try:
        gp = {a: (E.xs((ds, a, "Central-bal", "argmax"), level=["ds", "arm", "model", "rule"])
                  - E.xs((ds, a, "FedAvg-bal", "argmax"), level=["ds", "arm", "model", "rule"])) for a in ("e1", "primary")}
        e, ci = boot((gp["e1"] - gp["primary"]).dropna())
        print(f"- {ds}: {fmt(e, ci)} -> {'SUPPORTED' if ci[0] > 0 else 'NOT supported'}")
    except KeyError:
        print(f"- {ds}: not yet run")
print("\n## Owner view (owner's own class F1, primary alpha=0.5)\n")
o = d[(d.view == "owner") & (d.arm == "primary") & (d.alpha == 0.5)]
print(o.groupby(["ds", "k", "model"]).f1.mean().unstack().round(3).to_markdown())
print("\n## Sensitivity (rare F1, primary alpha=0.5, pooled over k): OC variants\n")
print(g[(g.arm == "primary") & (g.alpha == 0.5) & (g.group == "rare")].groupby(["ds", "rule", "model"]).f1.mean()
      .unstack("model").round(3).to_markdown())

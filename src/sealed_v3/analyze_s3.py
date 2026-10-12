"""Study 3 analysis (plan study_plan_robustness_v3_SEALED.md). Usage: python3 analyze_s3.py RUNDIR [OUT_CSV] > report.md"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef, roc_auc_score

Q = 1e-3
ROOT = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "..", "s3_scores.csv")


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


rows, far, mia, drift, cost, nused = [], [], [], [], [], []
for f in sorted(glob.glob(os.path.join(ROOT, "*.npz"))):
    ds, arm, seed, k = re.match(r"(\w+?)_(main|ip|big)_s(\d+)_k(\d+)\.npz", os.path.basename(f)).groups()
    z = np.load(f); cls = list(z["classes"]); rare = list(z["rare"]); y = z["y_test"]
    rid = [cls.index(c) for c in rare]; nrid = [i for i in range(len(cls)) if i not in rid]
    meta = dict(ds=ds, arm=arm, seed=int(seed), k=int(k)); own = z["owner"]; cut = np.cumsum(z["neg_sizes"])[:-1]
    negte = ~np.isin(y, rid)
    order = np.argsort(z["t_test"], kind="stable"); win = np.zeros(len(y), bool); win[order[: len(y) // 4]] = True
    for c, nu in zip(rare, z["n_used"]):
        nused.append(dict(meta, cls=c, n_used=int(nu)))
    for nm, s in zip(z["timing_names"], z["timing_secs"]):
        cost.append(dict(meta, method=str(nm), secs=float(s)))

    def score(pred, method, view="global", mask=None):
        mm = np.ones(len(y), bool) if mask is None else mask
        yy, pp = y[mm], pred[mm]
        for ci, c in enumerate(cls):
            p, r, f1 = prf(yy == ci, pp == ci)
            rows.append(dict(meta, method=method, view=view, cls=c, group="rare" if c in rare else ("benign" if ci == 0 else "common"),
                             precision=p, recall=r, f1=f1, mcc=np.nan))
        rows[-1]["mcc"] = matthews_corrcoef(yy, pp)
    for m in ("CCVR", "FedProx-bal", "GB+CR", "Central-bal", "FedOV", "FedOV-full"):
        L = z[f"{m}|test"]; score(L.argmax(1), f"{m} argmax")
        tv = [np.quantile(margin(z[f"{m}|cal"], c), 1 - Q) for c in rid]
        score(fuse(L, [margin(L, c) for c in rid], tv, rid, nrid), f"{m}+OC")
    G = z["GB+CR|test"]
    for v in ("", "_dp1", "_dp8"):
        S = [z[f"expert{v}_{c}|test"] for c in rare]
        tf, to = [], []
        for i, (c, ci) in enumerate(zip(rare, rid)):
            sa = z[f"expert{v}_{c}|negall"]; parts = np.split(sa, cut)
            tf.append(np.quantile(sa, 1 - Q)); to.append(np.quantile(parts[own[i]], 1 - Q))
            far.append(dict(meta, variant=v or "nonDP", cls=c, fed=(S[i][negte] >= tf[-1]).mean(), own=(S[i][negte] >= to[-1]).mean()))
            mem = z[f"expert{v}_{c}|mem"]; nm_ = z[f"expert{v}_{c}|nonmem"]
            if len(mem) and len(nm_):
                mia.append(dict(meta, variant=v or "nonDP", cls=c, auc=roc_auc_score(np.r_[np.ones(len(mem)), np.zeros(len(nm_))], np.r_[mem, nm_]), n=len(mem)))
        name = {"": "SAFE-X", "_dp1": "SAFE-X-DP eps1", "_dp8": "SAFE-X-DP eps8"}[v]
        score(fuse(G, S, tf, rid, nrid), name)
        if v == "":
            score(fuse(G, S, to, rid, nrid), "SAFE-X owner-only cal.")
            # Part D: static vs label-free recalibration on the earliest 25% of test traffic; evaluated on the rest
            tr_ = [np.quantile(s[win], 1 - Q) for s in S]; ev = ~win
            score(fuse(G, S, tf, rid, nrid), "SAFE-X static (eval 75%)", mask=ev)
            score(fuse(G, S, tr_, rid, nrid), "SAFE-X recalibrated (eval 75%)", mask=ev)
            for i, c in enumerate(rare):
                drift.append(dict(meta, cls=c, static=(S[i][ev & negte] >= tf[i]).mean(), recal=(S[i][ev & negte] >= tr_[i]).mean()))
    for i, (c, ci) in enumerate(zip(rare, rid)):
        p, r, f1 = prf(y == ci, z[f"expert_{c}|argmax_is_c"])
        rows.append(dict(meta, method="Owner alone", view="owner", cls=c, group="rare", precision=p, recall=r, f1=f1, mcc=np.nan))

d = pd.DataFrame(rows); d.to_csv(OUT, index=False)
fa, mi, dr, co = pd.DataFrame(far), pd.DataFrame(mia), pd.DataFrame(drift), pd.DataFrame(cost)
rng = np.random.default_rng(0)


def boot(v):
    v = np.asarray(v, float); bs = rng.choice(v, (4000, len(v))).mean(1)
    return v.mean(), np.percentile(bs, [2.5, 97.5])


def fmt(e, ci, s=100):
    return f"{s * e:+.1f} [{s * ci[0]:+.1f}, {s * ci[1]:+.1f}]"


g = d[d.view == "global"]
F = g.groupby(["ds", "arm", "k", "seed", "method", "group"]).f1.mean().unstack("group")
MCC = g.groupby(["ds", "arm", "k", "seed", "method"]).mcc.max()
print("# Study 3 results (plan v3)\n")
print("Units:", F.reset_index().groupby(["ds", "arm", "k"]).seed.nunique().to_dict(), "\n")
for (ds, arm), sub in F.rare.groupby(level=["ds", "arm"]):
    print(f"## {ds}, {arm}: rare F1 (seed means)\n"); print(sub.groupby(["k", "method"]).mean().unstack("k").round(3).to_markdown(), "\n")
    print(f"MCC (seed means)\n"); print(MCC.xs((ds, arm), level=["ds", "arm"]).groupby(["k", "method"]).mean().unstack("k").round(3).to_markdown(), "\n")
own = d[d.view == "owner"].groupby(["ds", "arm", "k"]).f1.mean().round(3)
print("Owner alone (own class):", own.to_dict(), "\n")


def pooled(sub, a, b):
    r = sub.unstack("method"); return (r[a] - r[b]).groupby(level="seed").mean()


print("## Part A: SAFE-X vs the better FedOV+OC (arm main)\n")
for ds, sub in F.rare.xs("main", level="arm").groupby(level="ds"):
    r = sub.unstack("method"); better = "FedOV-full+OC" if r["FedOV-full+OC"].mean() > r["FedOV+OC"].mean() else "FedOV+OC"
    e, ci = boot(pooled(sub, "SAFE-X", better))
    print(f"- A1 {ds}: better FedOV = {better}; SAFE-X - {better}: {fmt(e, ci)} -> {'SUPPORTED' if ci[0] > 0 else 'NOT supported'}")
    for kk, s2 in sub.groupby(level="k"):
        r2 = s2.unstack("method"); e, ci = boot(r2["SAFE-X"] - r2["FedOV-full+OC"])
        print(f"  - A2 {ds} k={kk}: SAFE-X - FedOV-full+OC {fmt(e, ci)}")
if "ip" in F.index.get_level_values("arm"):
    print("\n## Part B: destination-host sites (ToN)\n")
    sub = F.rare.xs(("ton", "ip"), level=["ds", "arm"]); ok = 0
    for kk, s2 in sub.groupby(level="k"):
        r2 = s2.unstack("method"); best = r2[["GB+CR argmax", "FedProx-bal argmax", "CCVR argmax"]].max(axis=1)
        e, ci = boot(r2["Central-bal argmax"] - best); ok += ci[0] > 0
        print(f"- B1 k={kk}: Central - best FL {fmt(e, ci)}")
    print(f"- B1: {'SUPPORTED' if ok >= 2 else 'NOT supported'}")
    e, ci = boot(pooled(sub, "SAFE-X", "FedOV+OC")); print(f"- B2: SAFE-X - FedOV+OC {fmt(e, ci)} -> {'SUPPORTED' if ci[0] > 0 else 'NOT supported'}")
    s = fa[(fa.arm == "ip") & (fa.variant == "nonDP")].groupby("seed")[["fed", "own"]].mean(); e, ci = boot(s.own - s.fed)
    print(f"- B3: owner-only {s.own.mean():.4f}, federated {s.fed.mean():.4f}; diff {fmt(e, ci, 1000)} per mille -> {'SUPPORTED' if ci[0] > 0 else 'NOT supported'}")
    print("  owner flows used:", pd.DataFrame(nused).query("arm == 'ip'").groupby(["k", "cls"]).n_used.agg(["min", "max"]).to_dict())
print("\n## Part C: privacy (arm main)\n")
for (ds, kk), sub in mi[mi.arm == "main"].groupby(["ds", "k"]):
    for v, s in sub.groupby("variant"):
        e, ci = boot(s.groupby("seed").auc.mean()); print(f"- C1 {ds} k={kk} {v}: MIA AUC {e:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]")
for ds, sub in F.rare.xs("main", level="arm").groupby(level="ds"):
    for v in ("SAFE-X-DP eps8", "SAFE-X-DP eps1"):
        e, ci = boot(pooled(sub, v, "FedOV+OC")); r = sub.unstack("method")
        print(f"- C2 {ds} {v}: rare F1 {r[v].mean():.3f} (SAFE-X {r['SAFE-X'].mean():.3f}); minus FedOV+OC {fmt(e, ci)}{' (claimed)' if ci[0] > 0 and v.endswith('eps8') else ''}")
for (ds, v), s in fa[fa.arm == "main"].groupby(["ds", "variant"]):
    print(f"  - false-alarm rate {ds} {v}: federated {s.fed.mean():.4f}")
print("\n## Part D: recalibration under drift (arm main)\n")
for ds, s in dr[dr.arm == "main"].groupby("ds"):
    ps = s.groupby("seed")[["static", "recal"]].mean(); e, ci = boot(ps.static - ps.recal)
    print(f"- D1 {ds}: static {s.static.mean():.4f}, recalibrated {s.recal.mean():.4f}; static - recal {fmt(e, ci, 1000)} per mille -> {'SUPPORTED' if ci[0] > 0 else 'NOT supported'}")
    gg = g[(g.ds == ds) & (g.arm == "main")]
    for m in ("SAFE-X static (eval 75%)", "SAFE-X recalibrated (eval 75%)"):
        x = gg[gg.method == m]
        print(f"  - {m}: rare F1 {x[x.group == 'rare'].f1.mean():.3f}; benign recall {x[x.group == 'benign'].recall.mean():.4f}")
if "big" in F.index.get_level_values("arm"):
    print("\n## Part E: larger model (k = 20)\n")
    print(F.rare.xs("big", level="arm").groupby(["ds", "method"]).mean().unstack("ds").round(3).to_markdown())
print("\n## Cost: median training seconds per run\n")
print(co.groupby(["ds", "arm", "method"]).secs.median().unstack(["ds", "arm"]).round(0).to_markdown())

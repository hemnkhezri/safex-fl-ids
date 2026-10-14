"""Study 4 analysis (plan study_plan_scale_v4_SEALED.md).
Parts G (K = 20, 50) and H (2 or 3 owners per rare class) from RUNDIR; Part I (q sensitivity) from the Study 3 main-arm runs in S3DIR.
Usage: python3 analyze_s4.py RUNDIR S3DIR OUT_PREFIX > report.md
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef

ROOT, S3, OUTP = sys.argv[1], sys.argv[2], sys.argv[3]
Q = 1e-3
QS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
BASE = ("CCVR", "FedProx-bal", "GB+CR", "Central-bal", "FedOV", "FedOV-full")


def margin(L, c):
    o = L.astype(np.float32).copy(); o[:, c] = -np.inf
    return L[:, c].astype(np.float32) - o.max(1)


def prf(m, pr):
    tp = (pr & m).sum(); p = tp / max(pr.sum(), 1); r = tp / max(m.sum(), 1)
    return p, r, (0 if p + r == 0 else 2 * p * r / (p + r))


def fuse(G, excess, rid, nrid):
    """excess: list (one per rare class) of score minus threshold; any >= 0 overrides the global model."""
    pred = np.array(nrid)[G[:, nrid].argmax(1)]
    ex = np.stack(excess, 1); hit = ex.max(1) >= 0
    pred[hit] = np.array(rid)[ex[hit].argmax(1)]
    return pred


def score_rows(rows, meta, y, pred, cls, rare, method):
    for ci, c in enumerate(cls):
        p, r, f1 = prf(y == ci, pred == ci)
        rows.append(dict(meta, method=method, cls=c, group="rare" if c in rare else ("benign" if ci == 0 else "common"),
                         precision=p, recall=r, f1=f1, mcc=np.nan))
    rows[-1]["mcc"] = matthews_corrcoef(y, pred)


# ------------------------------------------------------------------ Parts G and H
rows, far = [], []
for f in sorted(glob.glob(os.path.join(ROOT, "*.npz"))):
    ds, arm, seed, k = re.match(r"(\w+?)_(K\d+|own\d)_s(\d+)_k(\d+)\.npz", os.path.basename(f)).groups()
    z = np.load(f); cls = list(z["classes"]); rare = list(z["rare"]); y = z["y_test"]; m = int(z["m"])
    rid = [cls.index(c) for c in rare]; nrid = [i for i in range(len(cls)) if i not in rid]
    meta = dict(ds=ds, arm=arm, seed=int(seed), k=int(k)); cut = np.cumsum(z["neg_sizes"])[:-1]; negte = ~np.isin(y, rid)
    owners = z["owners"]
    for mname in BASE:
        L = z[f"{mname}|test"].astype(np.float32); score_rows(rows, meta, y, L.argmax(1), cls, rare, f"{mname} argmax")
        tv = [np.quantile(margin(z[f"{mname}|cal"], c), 1 - Q) for c in rid]
        score_rows(rows, meta, y, fuse(L, [margin(L, c) - t for c, t in zip(rid, tv)], rid, nrid), cls, rare, f"{mname}+OC")
    G = z["GB+CR|test"].astype(np.float32)
    # SAFE-X: one expert per owner; each expert's threshold is its federated (1 - q/m) quantile; a class's excess is the max over its owners
    exf, exo = [], []
    for i, (c, ci) in enumerate(zip(rare, rid)):
        ef, eo = [], []
        for o in range(m):
            S = z[f"expert_{c}_o{o}|test"]; sa = z[f"expert_{c}_o{o}|negall"]
            tf = np.quantile(sa, 1 - Q / m); to = np.quantile(np.split(sa, cut)[owners[i][o]], 1 - Q / m)
            ef.append(S - tf); eo.append(S - to)
        ef, eo = np.max(ef, 0), np.max(eo, 0); exf.append(ef); exo.append(eo)
        far.append(dict(meta, cls=c, fed=(ef[negte] >= 0).mean(), own=(eo[negte] >= 0).mean()))
        for o in range(m):
            p, r, f1 = prf(y == ci, z[f"expert_{c}_o{o}|argmax_is_c"])
            rows.append(dict(meta, method="Owner alone", cls=c, group="owner", precision=p, recall=r, f1=f1, mcc=np.nan))
    score_rows(rows, meta, y, fuse(G, exf, rid, nrid), cls, rare, "SAFE-X")
    score_rows(rows, meta, y, fuse(G, exo, rid, nrid), cls, rare, "SAFE-X owner-only cal.")

d = pd.DataFrame(rows); d.to_csv(OUTP + "_scores.csv", index=False)
fa = pd.DataFrame(far); fa.to_csv(OUTP + "_far.csv", index=False)
rng = np.random.default_rng(0)


def boot(v):
    v = np.asarray(v, float); bs = rng.choice(v, (4000, len(v))).mean(1)
    return v.mean(), np.percentile(bs, [2.5, 97.5])


def fmt(e, ci, s=100):
    return f"{s * e:+.1f} [{s * ci[0]:+.1f}, {s * ci[1]:+.1f}]"


g = d[d.group != "owner"]
F = g.groupby(["ds", "arm", "seed", "method", "group"]).f1.mean().unstack("group")
MCC = g.groupby(["ds", "arm", "seed", "method"]).mcc.max()
print("# Study 4 results (plan v4)\n")
print("Units:", F.reset_index().groupby(["ds", "arm"]).seed.nunique().to_dict(), "\n")
for arm, sub in F.rare.groupby(level="arm"):
    print(f"## {arm}: rare-class F1 (seed means, k = 20)\n"); print(sub.groupby(["method", "ds"]).mean().unstack("ds").round(3).to_markdown(), "\n")
    print("MCC\n"); print(MCC.xs(arm, level="arm").groupby(["method", "ds"]).mean().unstack("ds").round(3).to_markdown(), "\n")
own = d[d.group == "owner"].groupby(["ds", "arm"]).f1.mean().round(3)
print("Owner alone (own class):", own.to_dict(), "\n")
FL = ["GB+CR argmax", "FedProx-bal argmax", "CCVR argmax"]


def better_fedov(r):
    return "FedOV-full+OC" if r["FedOV-full+OC"].mean() > r["FedOV+OC"].mean() else "FedOV+OC"


res = {}
for part, arms in (("G", ["K20", "K50"]), ("H", ["own2", "own3"])):
    print(f"## Part {part}\n")
    n1 = n2 = n3 = 0; tot = 0
    for arm in arms:
        if arm not in F.index.get_level_values("arm"):
            continue
        for ds, sub in F.rare.xs(arm, level="arm").groupby(level="ds"):
            r = sub.unstack("method").droplevel("ds"); tot += 1
            e1, c1 = boot(r["Central-bal argmax"] - r[FL].max(axis=1)); n1 += c1[0] > 0
            b = better_fedov(r); e2, c2 = boot(r["SAFE-X"] - r[b]); n2 += c2[0] > 0
            bo = max(["CCVR+OC", "GB+CR+OC", "FedProx-bal+OC"], key=lambda x: r[x].mean()); e4, c4 = boot(r["SAFE-X"] - r[bo])
            s = fa[(fa.arm == arm) & (fa.ds == ds)].groupby("seed")[["fed", "own"]].mean(); e3, c3 = boot(s.own - s.fed); n3 += c3[0] > 0
            cm = F.common.xs(arm, level="arm").xs(ds, level="ds").unstack("method"); e5, c5 = boot(cm["SAFE-X"] - cm["GB+CR argmax"])
            print(f"- {ds} {arm}: {part}1 gap Central - best FL {fmt(e1, c1)}; {part}2 SAFE-X - {b} {fmt(e2, c2)}; "
                  f"SAFE-X - {bo} {fmt(e4, c4)}; {part}3 FA owner-only {s.own.mean():.4f} vs federated {s.fed.mean():.4f}, diff {fmt(e3, c3, 1000)} per mille; "
                  f"common F1 SAFE-X - GB+CR {fmt(e5, c5)}")
    if tot:
        if part == "G":
            print(f"\n- G1 {'SUPPORTED' if n1 >= 4 else 'NOT supported'} ({n1}/{tot}); G2 {'SUPPORTED' if n2 >= 4 else 'NOT supported'} ({n2}/{tot}); "
                  f"G3 {'SUPPORTED' if n3 >= 4 else 'NOT supported'} ({n3}/{tot})\n")
        else:
            print(f"\n- H (descriptive): gap CI above 0 in {n1}/{tot}; SAFE-X ahead of better FedOV+OC with CI above 0 in {n2}/{tot}\n")

# ------------------------------------------------------------------ Part I: q sensitivity on Study 3 main-arm runs
qrows = []
for f in sorted(glob.glob(os.path.join(S3, "*_main_s*_k*.npz"))):
    ds, seed, k = re.match(r"(\w+?)_main_s(\d+)_k(\d+)\.npz", os.path.basename(f)).groups()
    z = np.load(f); cls = list(z["classes"]); rare = list(z["rare"]); y = z["y_test"]
    rid = [cls.index(c) for c in rare]; nrid = [i for i in range(len(cls)) if i not in rid]; negte = ~np.isin(y, rid)
    G = z["GB+CR|test"]; Gp = np.array(nrid)[G[:, nrid].argmax(1)]
    S = [z[f"expert_{c}|test"] for c in rare]; SA = [z[f"expert_{c}|negall"] for c in rare]
    base = {mn: (z[f"{mn}|test"], [margin(z[f"{mn}|cal"], c) for c in rid]) for mn in ("CCVR", "FedOV", "FedOV-full")}
    for q in QS:
        meta = dict(ds=ds, seed=int(seed), k=int(k), q=q)
        tf = [np.quantile(sa, 1 - q) for sa in SA]
        preds = {"SAFE-X": fuse(G, [s - t for s, t in zip(S, tf)], rid, nrid)}
        for mn, (L, cm) in base.items():
            preds[f"{mn}+OC"] = fuse(L, [margin(L, c) - np.quantile(m_, 1 - q) for c, m_ in zip(rid, cm)], rid, nrid)
        for mn, pr in preds.items():
            rr = [prf(y == ci, pr == ci) for ci in rid]; cc = [prf(y == ci, pr == ci)[2] for ci in range(1, len(cls)) if ci not in rid]
            qrows.append(dict(meta, method=mn, rare_f1=np.mean([x[2] for x in rr]), rare_p=np.mean([x[0] for x in rr]),
                              rare_r=np.mean([x[1] for x in rr]), common_f1=np.mean(cc),
                              common_f1_gbcr=np.mean([prf(y == ci, Gp == ci)[2] for ci in range(1, len(cls)) if ci not in rid]),
                              fa=np.mean([(s[negte] >= t).mean() for s, t in zip(S, tf)]) if mn == "SAFE-X" else np.nan))
qd = pd.DataFrame(qrows); qd.to_csv(OUTP + "_qsens.csv", index=False)
if len(qd):
    print("## Part I: sensitivity to q (Study 3 main-arm runs, pooled over k)\n")
    print(qd.groupby(["ds", "method", "q"]).rare_f1.mean().unstack("q").round(3).to_markdown(), "\n")
    s = qd[qd.method == "SAFE-X"].assign(dcommon=lambda x: x.common_f1 - x.common_f1_gbcr)
    print("SAFE-X: expert false-alarm rate, rare precision and common-F1 change vs GB+CR\n")
    print(s.groupby(["ds", "q"])[["fa", "rare_p", "rare_r", "dcommon"]].mean().round(4).to_markdown(), "\n")
    for ds, sub in qd.groupby("ds"):
        for q, s2 in sub.groupby("q"):
            r = s2.pivot_table(index=["seed", "k"], columns="method", values="rare_f1")
            b = "FedOV-full+OC" if r["FedOV-full+OC"].mean() > r["FedOV+OC"].mean() else "FedOV+OC"
            e, ci = boot((r["SAFE-X"] - r[b]).groupby(level="seed").mean())
            print(f"- I1 {ds} q={q:g}: SAFE-X - {b} {fmt(e, ci)}")

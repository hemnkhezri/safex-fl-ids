"""Study 5 analysis (sealed plan study_plan_aci_v5_SEALED.md; seeds 500-509). Usage: python3 analyze_study5.py RUNDIR OUT_PREFIX > report.md
Same scoring code as analyze_pilot8.py; adds the sealed tests J1-J4 at gamma = 0.005.
Variants, all fused with the GB+CR global model as in SAFE-X (Eq. 3):
  SAFE-X               plain owner expert, pooled federated calibration at q (as in the paper)
  SAFE-X per-group     plain expert, threshold = max of the (1-q) quantiles on benign and on common-attack negatives
  SAFE-X frozen        expert = global GB+CR encoder frozen, head trained at the owner; pooled federated calibration
  SAFE-X ACI g         plain expert; adaptive conformal inference on the time-ordered test stream with analyst feedback:
                       only alarms are labelled; alpha_{t+1} = alpha_t + g (q - err_t), err_t = 1[alarm and flow is not class c],
                       threshold_t = (1 - alpha_t) quantile of the federated calibration scores
  FedOV(-full)+OC      the better FedOV variant with validation calibration; and the same with ACI
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

ROOT, OUTP = sys.argv[1], sys.argv[2]
Q, GAMMAS = 1e-3, (0.005, 0.02, 0.05)


def margin(L, c):
    L = L.astype(np.float32); o = L.copy(); o[:, c] = -np.inf
    return L[:, c] - o.max(1)


def prf(m, pr):
    tp = (pr & m).sum(); p = tp / max(pr.sum(), 1); r = tp / max(m.sum(), 1)
    return p, r, (0 if p + r == 0 else 2 * p * r / (p + r))


def fuse(G, hits, ex, rid, nrid):
    """hits/ex: (n, |R|) boolean alarms and excess scores; the alarm with the largest excess wins."""
    pred = np.array(nrid)[G[:, nrid].argmax(1)]; anyh = hits.any(1)
    e = np.where(hits, ex, -np.inf); pred[anyh] = np.array(rid)[e[anyh].argmax(1)]
    return pred


def aci(s, is_c, order, cal_sorted, g, q=Q):
    """Online threshold: returns alarm vector (in original order) and excess s - tau_t."""
    n = len(cal_sorted); a = q; alarm = np.zeros(len(s), bool); ex = np.zeros(len(s), np.float32)
    for t in order:
        if a <= 0:
            tau = np.inf
        elif a >= 1:
            tau = -np.inf
        else:
            tau = cal_sorted[min(n - 1, int(np.floor((1 - a) * n)))]
        hit = s[t] >= tau; alarm[t] = hit; ex[t] = s[t] - tau if np.isfinite(tau) else (-1.0 if tau > 0 else 1.0)
        a += g * (q - float(hit and not is_c[t]))
    return alarm, ex


rows = []
for f in sorted(glob.glob(os.path.join(ROOT, "*.npz"))):
    ds, seed = re.match(r"(\w+?)_s(\d+)\.npz", os.path.basename(f)).groups()
    z = np.load(f); cls = list(z["classes"]); rare = list(z["rare"]); y = z["y_test"]
    rid = [cls.index(c) for c in rare]; nrid = [i for i in range(len(cls)) if i not in rid]
    negte = ~np.isin(y, rid); bente = y == 0; comte = negte & ~bente
    order = np.argsort(z["t_test"], kind="stable"); yn = z["y_negall"]
    G = z["GB+CR|test"].astype(np.float32); Gp = np.array(nrid)[G[:, nrid].argmax(1)]
    variants = {}
    for kind in ("plain", "frozen"):
        S = [z[f"{kind}_{c}|test"].astype(np.float32) for c in rare]; SA = [z[f"{kind}_{c}|negall"].astype(np.float32) for c in rare]
        tp = [np.quantile(sa, 1 - Q) for sa in SA]
        variants[f"SAFE-X{'' if kind == 'plain' else ' frozen'}"] = [(s >= t, s - t) for s, t in zip(S, tp)]
        if kind == "plain":
            tg = [max(np.quantile(sa[yn == 0], 1 - Q), np.quantile(sa[yn != 0], 1 - Q)) for sa in SA]
            variants["SAFE-X per-group"] = [(s >= t, s - t) for s, t in zip(S, tg)]
            for g in GAMMAS:
                variants[f"SAFE-X ACI {g}"] = [aci(s, y == ci, order, np.sort(sa), g) for s, sa, ci in zip(S, SA, rid)]
    best = max(("FedOV", "FedOV-full"), key=lambda m: np.mean([prf(y == ci, (margin(z[f"{m}|test"], ci) >= np.quantile(margin(z[f"{m}|cal"], ci), 1 - Q))) [2] for ci in rid]))
    Lt, Lc = z[f"{best}|test"].astype(np.float32), z[f"{best}|cal"]
    Mt = [margin(Lt, ci) for ci in rid]; Mc = [margin(Lc, ci) for ci in rid]
    variants["FedOV+OC"] = [(m >= np.quantile(mc, 1 - Q), m - np.quantile(mc, 1 - Q)) for m, mc in zip(Mt, Mc)]
    for g in GAMMAS:
        variants[f"FedOV+OC ACI {g}"] = [aci(m, y == ci, order, np.sort(mc), g) for m, mc, ci in zip(Mt, Mc, rid)]
    half = np.zeros(len(y), bool); half[order[len(order) // 2:]] = True
    for vname, lst in variants.items():
        hits = np.stack([h for h, _ in lst], 1); ex = np.stack([e for _, e in lst], 1)
        G_ = Lt if vname.startswith("FedOV") else G
        pred = fuse(G_, hits, ex, rid, nrid)
        rr = [prf(y == ci, pred == ci) for ci in rid]
        cc = np.mean([prf(y == ci, pred == ci)[2] for ci in nrid if ci != 0])
        cg = np.mean([prf(y == ci, Gp == ci)[2] for ci in nrid if ci != 0])
        rows.append(dict(ds=ds, seed=int(seed), method=vname, fedov=best, rare_f1=np.mean([r[2] for r in rr]),
                         rare_p=np.mean([r[0] for r in rr]), rare_r=np.mean([r[1] for r in rr]), common_f1=cc, common_f1_gbcr=cg,
                         fa=hits[negte].mean(), fa_benign=hits[bente].mean(), fa_common=hits[comte].mean(),
                         fa_2nd_half=hits[negte & half].mean(), benign_recall=(pred[bente] == 0).mean()))
        if vname in ("SAFE-X", "SAFE-X frozen"):
            k = "plain" if vname == "SAFE-X" else "frozen"
            for c, ci in zip(rare, rid):
                rows.append(dict(ds=ds, seed=int(seed), method=f"Owner alone ({k})", rare_f1=prf(y == ci, z[f"{k}_{c}|owner_argmax"])[2]))

d = pd.DataFrame(rows); d.to_csv(OUTP + "_scores.csv", index=False)
rng = np.random.default_rng(0)


def boot(v):
    v = np.asarray(v, float); b = rng.choice(v, (4000, len(v))).mean(1)
    return f"{100 * v.mean():+.1f} [{100 * np.percentile(b, 2.5):+.1f}, {100 * np.percentile(b, 97.5):+.1f}]"


G = "0.005"
print("# Study 5: ACI with analyst feedback (seeds 500-509, k = 20, K = 10; sealed)\n")
print("Seeds per dataset:", d.groupby("ds").seed.nunique().to_dict(), "\n")
m = d.groupby(["ds", "method"])[["rare_f1", "rare_p", "rare_r", "fa", "fa_benign", "fa_common", "fa_2nd_half", "benign_recall"]].mean()
m["d_common_f1"] = (d.common_f1 - d.common_f1_gbcr).groupby([d.ds, d.method]).mean()
print("## Seed means (FA target 0.001)\n"); print(m.round(4).to_markdown(), "\n")


def ci(v):
    v = np.asarray(v, float); b = rng.choice(v, (4000, len(v))).mean(1)
    return v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5)


A, S, FA = f"SAFE-X ACI {G}", "SAFE-X", f"FedOV+OC ACI {G}"
print("## Sealed tests\n")
print("| Dataset | J1 FA overall | J1 FA 2nd half | J1 | J2 ACI - SAFE-X (F1 pts) | J2 | J3 common F1 vs GB+CR (pts) | J3 | J4 ACI - FedOV+OC ACI (pts) | J4 |")
print("|---|---|---|---|---|---|---|---|---|---|")
cnt = dict(J1=0, J2=0, J3=0, J4=0)
for ds in sorted(d.ds.unique()):
    x = d[d.ds == ds]; P = x.pivot_table(index="seed", columns="method", values="rare_f1")
    a = x[x.method == A].set_index("seed")
    fa, fa2 = a.fa.mean(), a.fa_2nd_half.mean(); j1 = fa <= 0.0012 and fa2 <= 0.0012
    j2 = ci(P[A] - P[S]); j3 = ci(a.common_f1 - a.common_f1_gbcr); j4 = ci(P[A] - P[FA])
    r = dict(J1=j1, J2=j2[1] > -0.03, J3=j3[1] > -0.01, J4=j4[1] > 0)
    for k in cnt: cnt[k] += int(r[k])
    f = lambda t: f"{100*t[0]:+.1f} [{100*t[1]:+.1f}, {100*t[2]:+.1f}]"; yn = lambda b: "supported" if b else "not supported"
    print(f"| {ds} | {100*fa:.3f}% | {100*fa2:.3f}% | {yn(r['J1'])} | {f(j2)} | {yn(r['J2'])} | {f(j3)} | {yn(r['J3'])} | {f(j4)} | {yn(r['J4'])} |")
print("\nSupported on datasets (of 3):", cnt, "\n")
print("## Other paired differences in rare F1 (descriptive)\n")
for ds, r in F.groupby(level="ds") if False else []:
    pass
F = d.pivot_table(index=["ds", "seed"], columns="method", values="rare_f1")
for ds, r in F.groupby(level="ds"):
    print(f"- {ds}: SAFE-X - FedOV+OC {boot(r['SAFE-X'] - r['FedOV+OC'])}; {A} - FedOV+OC {boot(r[A] - r['FedOV+OC'])}")

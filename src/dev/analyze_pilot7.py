"""Summarise pilot 7 (development seeds; exploratory). Usage: python3 analyze_pilot7.py DIR > report.md"""
import glob
import os
import sys

import numpy as np
import pandas as pd

D = sys.argv[1]
sc = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(D, "*_scores.csv")))])
fa = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(D, "*_far.csv")))])
rng = np.random.default_rng(0)


def boot(v):
    v = np.asarray(v, float); b = rng.choice(v, (4000, len(v))).mean(1)
    return f"{100 * v.mean():+.1f} [{100 * np.percentile(b, 2.5):+.1f}, {100 * np.percentile(b, 97.5):+.1f}]"


print("# Pilot 7: SAFE-X extensions (development seeds 0-4, k = 20, K = 10; exploratory, no claims)\n")
print("Seeds per dataset:", sc.groupby("ds").seed.nunique().to_dict(), "\n")
info = sc[sc.group == "info"]
print("Cascade gate (GB+CR p_benign < 0.5): share of rare test flows passing", info.groupby("ds").recall.mean().round(3).to_dict(),
      "; share of calibration negatives passing", info.groupby("ds").f1.mean().round(3).to_dict(), "\n")
s = sc[sc.group != "info"]
R = s[s.group == "rare"].groupby(["ds", "seed", "method"])[["precision", "recall", "f1"]].mean()
print("## Rare-class precision / recall / F1 (seed means)\n")
print(R.groupby(["ds", "method"]).mean().round(3).to_markdown(), "\n")
CM = s[s.group == "common"].groupby(["ds", "seed", "method"]).f1.mean().unstack("method")
print("## Common-attack F1 minus GB+CR argmax\n")
print((CM.sub(CM["GB+CR argmax"], axis=0)).groupby("ds").mean().round(3).T.to_markdown(), "\n")
print("## Expert false-alarm rate on non-rare test flows (target q = 0.001), mean over rare classes\n")
print(fa.groupby(["ds", "method"])[["fa", "fa_benign", "recall_expert"]].mean().round(4).to_markdown(), "\n")
print("Per class:\n"); print(fa.groupby(["ds", "cls", "method"]).fa.mean().unstack("method").round(4).to_markdown(), "\n")
print("## Paired differences in rare F1 (points, bootstrap over seeds)\n")
F = R.f1.unstack("method")
for ds, r in F.groupby(level="ds"):
    bf = "FedOV-full+OC" if r["FedOV-full+OC"].mean() > r["FedOV+OC"].mean() else "FedOV+OC"
    for v in ("SAFE-X+NR", "SAFE-X+cascade", "SAFE-X+NR+cascade"):
        print(f"- {ds}: {v} - SAFE-X {boot(r[v] - r['SAFE-X'])}; {v} - {bf} {boot(r[v] - r[bf])}")
    print(f"- {ds}: SAFE-X - {bf} {boot(r['SAFE-X'] - r[bf])}")

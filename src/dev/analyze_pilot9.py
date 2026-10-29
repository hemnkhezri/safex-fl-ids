"""Summarise pilot 9 (development seeds; exploratory, no claims). Usage: python3 analyze_pilot9.py RUNDIR > report.md"""
import glob
import os
import sys

import numpy as np
import pandas as pd

d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.csv")))])
rng = np.random.default_rng(0)


def boot(v):
    v = np.asarray(v, float); b = rng.choice(v, (4000, len(v))).mean(1)
    return f"{100 * v.mean():+.1f} [{100 * np.percentile(b, 2.5):+.1f}, {100 * np.percentile(b, 97.5):+.1f}]"


print("# Pilot 9: SAFE-X with a federated feedback loop (development seeds 0-4, k = 20, K = 10, ACI gamma = 0.005; exploratory, no claims)\n")
print("Seeds per dataset:", d.groupby("ds").seed.nunique().to_dict(), "\n")
cols = ["rare_f1", "rare_p", "rare_r", "rare_f1_2nd_half", "fa", "fa_2nd_half", "d_common_f1", "alarms_labelled"]
print("## Seed means\n"); print(d.groupby(["ds", "method"])[cols].mean().round(4).to_markdown(), "\n")
print("## Paired differences (F1 points, bootstrap over seeds)\n")
for col in ("rare_f1", "rare_f1_2nd_half"):
    F = d.pivot_table(index=["ds", "seed"], columns="method", values=col)
    for ds, r in F.groupby(level="ds"):
        print(f"- {ds} {col}: loop - static {boot(r['loop'] - r['static'])}; loopneg - static {boot(r['loopneg'] - r['static'])}; "
              f"loop - FedOV+OC ACI {boot(r['loop'] - r['FedOV+OC ACI'])}; static - FedOV+OC ACI {boot(r['static'] - r['FedOV+OC ACI'])}")

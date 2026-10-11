"""Stop rule for pilot 2: rare-class F1 gap = best centralised reference minus best global-view FL method
(including the known fixes). Go only if the gap is >= 10 F1 points (CI over seeds above 0) in some setting.
Owner view reported separately: FedRep and Local-owner on the owner's own rare class.
"""
import sys

import numpy as np
import pandas as pd

d = pd.read_csv(sys.argv[1]); r = d[d.rare]
G = ["FedAvg", "FedAvg-bal", "FedLC", "CCVR", "Proto-count-bal"]; CEN = ["Central-head", "Central-bal", "Central-proto"]
rng = np.random.default_rng(0)


def boot(g, col):
    s = g.seed.unique(); e = g.groupby("seed")[col].mean().mean()
    bs = [g[g.seed.isin(rng.choice(s, len(s)))].groupby("seed")[col].mean().mean() for _ in range(2000)]
    return e, np.percentile(bs, [2.5, 97.5])


print("# Pilot 2 result\n\n## Rare-class F1, global view (mean over 4 rare classes and 5 seeds)\n")
print(r[r.view == "global"].groupby(["alpha", "k", "method"]).f1.mean().unstack().round(3).to_markdown(), "\n")
print("## Rare-class precision / recall, global view (k pooled)\n")
print(r[r.view == "global"].groupby(["method"])[["precision", "recall"]].mean().round(3).to_markdown(), "\n")
print("## Owner view: owner's model on its own rare class (F1)\n")
ow = pd.concat([r[r.view == "owner"], r[(r.view == "global") & r.method.isin(["CCVR", "FedLC"])]])
print(ow.groupby(["alpha", "k", "method"]).f1.mean().unstack().round(3).to_markdown(), "\n")
p = r[r.view == "global"].pivot_table(index=["seed", "alpha", "k", "cls"], columns="method", values="f1").reset_index()
p["gap"] = p[CEN].max(axis=1) - p[G].max(axis=1)
p["best_fix_minus_fedavg"] = p[["FedAvg-bal", "FedLC", "CCVR"]].max(axis=1) - p["FedAvg"]
print("## F1 gap = best centralised - best global FL incl. fixes (x100), 95% CI over seeds\n")
for (a, k), g in p.groupby(["alpha", "k"]):
    e, ci = boot(g, "gap"); e2, ci2 = boot(g, "best_fix_minus_fedavg")
    print(f"- alpha={a}, k={k}: gap {100*e:+.1f} [{100*ci[0]:+.1f}, {100*ci[1]:+.1f}]; "
          f"best fix - FedAvg {100*e2:+.1f} [{100*ci2[0]:+.1f}, {100*ci2[1]:+.1f}]")
o = d[d.cls == "_overall"].groupby(["alpha", "k", "method"])[["f1", "mcc"]].mean()
print("\n## Overall macro-F1 and MCC\n"); print(o.unstack().round(3).to_markdown())

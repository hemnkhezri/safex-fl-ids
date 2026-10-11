"""Apply the pilot stop rule (pilot_design_v1.md section 1) to results/pilot_full.csv.
Gap(c) = recall of the better centralised variant (head or prototype) minus recall of the best FL method,
per seed and setting; CIs by bootstrap over seeds (seed = cluster).
"""
import sys

import numpy as np
import pandas as pd

d = pd.read_csv(sys.argv[1])
FL = ["FedAvg", "FedProx", "Proto-count", "Proto-discrepancy", "Proto-confidence"]
r = d[d.rare]
piv = r.pivot_table(index=["seed", "alpha", "k", "cls"], columns="method", values="recall").reset_index()
piv["central"] = piv[["Central-head", "Central-proto"]].max(axis=1)
piv["best_fl"] = piv[FL].max(axis=1)
piv["gap"] = piv.central - piv.best_fl
piv["disc_minus_count"] = piv["Proto-discrepancy"] - piv["Proto-count"]
rng = np.random.default_rng(0)


def boot(df, col):
    seeds = df.seed.unique()
    est = df.groupby("seed")[col].mean().mean()
    bs = [df[df.seed.isin(rng.choice(seeds, len(seeds)))].groupby("seed")[col].mean().mean() for _ in range(2000)]
    return est, np.percentile(bs, [2.5, 97.5])


print("# Pilot result\n")
print("## Mean recall of client-exclusive rare classes (over classes and seeds)\n")
print(r.groupby(["alpha", "k", "method"]).recall.mean().unstack().round(3).to_markdown(), "\n")
r = r.assign(f1=2 * r.recall * r.precision / (r.recall + r.precision).replace(0, np.nan))
print("## Mean precision and F1 of rare classes (recall alone can hide false alarms)\n")
print(r.groupby(["k", "method"])[["precision", "f1"]].mean().unstack().round(3).to_markdown(), "\n")
ben = d[d.cls == "Benign"].groupby(["k", "method"]).recall.mean()
print("## Benign recall (1 - false-alarm rate on benign)\n"); print(ben.unstack().round(4).to_markdown(), "\n")
print("## Per class (alpha pooled)\n")
print(r.groupby(["cls", "k", "method"]).recall.mean().unstack().round(3).to_markdown(), "\n")
print("## Gap = best centralised - best FL (recall points x100), 95% CI over seeds\n")
for (a, k), g in piv.groupby(["alpha", "k"]):
    e, ci = boot(g, "gap"); e2, ci2 = boot(g, "disc_minus_count")
    print(f"- alpha={a}, k={k}: gap {100*e:+.1f} [{100*ci[0]:+.1f}, {100*ci[1]:+.1f}]; "
          f"discrepancy - count {100*e2:+.1f} [{100*ci2[0]:+.1f}, {100*ci2[1]:+.1f}]")
o = d[d.cls == "_overall"].groupby(["alpha", "k", "method"]).agg(macroF1=("recall", "mean"), MCC=("precision", "mean"))
print("\n## Overall macro-F1 and MCC\n")
print(o.round(3).to_markdown())

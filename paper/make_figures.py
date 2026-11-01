import sys
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.6, "legend.frameon": False, "lines.linewidth": 1.6})
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"]
MK = ["o", "s", "^", "D", "v", "P"]
DSN = {"unsw": "NF-UNSW-NB15-v3", "ton": "NF-ToN-IoT-v3"}
rng = np.random.default_rng(0)
def ci(v):
    v = np.asarray(v); b = rng.choice(v, (4000, len(v))).mean(1); return v.mean(), *np.percentile(b, [2.5, 97.5])
FL = ["FedAvg", "FedAvg-bal", "FedProx-bal", "FedLC", "FedRS", "CCVR", "GB+CR"]

def panel(ax, series, title):
    ks = [5, 20, 100]
    for i, (name, per_k) in enumerate(series):
        m = [ci(per_k[k]) for k in ks]; mu = [x[0] for x in m]
        ax.errorbar(ks, mu, yerr=[[x[0] - x[1] for x in m], [x[2] - x[0] for x in m]], color=C[i], marker=MK[i], ms=4.5,
                    capsize=2, label=name, lw=1.4, elinewidth=0.9)
    ax.set_xscale("log"); ax.set_xticks(ks); ax.set_xticklabels(ks); ax.minorticks_off()
    ax.set_xlabel("Labeled flows per rare class at its owner (k)"); ax.set_title(title, fontsize=8.5, loc="left")

# Fig 2: Study 1
d = pd.read_csv(os.path.join(R, "study1", "conf_scores.csv")); d = d[(d.arm == "primary") & (d.alpha == 0.5)]
g = d[d.view == "global"].groupby(["ds", "k", "seed", "model", "rule", "group"]).f1.mean().unstack("group").rare.unstack(["model", "rule"])
own = d[(d.view == "owner") & (d.model == "Local-owner-bal")].groupby(["ds", "k", "seed"]).f1.mean()
fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0), sharey=False)
for ax, ds in zip(axs, ["unsw", "ton"]):
    s = g.xs(ds, level="ds")
    pk = lambda col: {k: s.xs(k, level="k")[col].values for k in [5, 20, 100]}
    best = s[[(m, "argmax") for m in FL]].max(axis=1)
    series = [("Central-bal (pooled data)", pk(("Central-bal", "argmax"))),
              ("Best federated, per seed", {k: best.xs(k, level="k").values for k in [5, 20, 100]}),
              ("CCVR + OC", pk(("CCVR", "OC q=0.001"))),
              ("Owner's local model (own class)", {k: own.xs((ds, k)).values for k in [5, 20, 100]})]
    panel(ax, series, DSN[ds]); ax.set_ylabel("Rare-class F1")
h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=2,fontsize=7)
fig.tight_layout(rect=(0,0.14,1,1)); fig.savefig(OUT + "/fig2_gap.pdf"); fig.savefig(OUT + "/fig2_gap.png", dpi=600); plt.close(fig)

# Fig 3: precision/recall split (argmax, all k)
pr = d[(d.view == "global") & (d.group == "rare") & (d.rule == "argmax")].groupby(["ds", "k", "model"])[["precision", "recall"]].mean()
fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0))
models = ["CCVR", "GB+CR", "FedProx-bal", "FedLC", "FedAvg-bal", "Central-bal"]
for ax, ds in zip(axs, ["unsw", "ton"]):
    for i, m in enumerate(models):
        x = pr.xs(ds, level="ds").xs(m, level="model")
        ax.plot(x.recall, x.precision, marker=MK[i], color=C[i], ms=5, lw=0.9, label=m, alpha=0.95)
        ax.annotate("k=100", (x.recall.iloc[-1], x.precision.iloc[-1]), fontsize=6.5, color="#52514e", xytext=(3, 2), textcoords="offset points") if m in ("CCVR", "GB+CR") else None
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel("Rare-class recall"); ax.set_ylabel("Rare-class precision")
    ax.set_title(DSN[ds], fontsize=8.5, loc="left")
h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=6,fontsize=7)
fig.tight_layout(rect=(0,0.08,1,1)); fig.savefig(OUT + "/fig3_split.pdf"); fig.savefig(OUT + "/fig3_split.png", dpi=600); plt.close(fig)

# Fig 4: Study 2
e = pd.read_csv(os.path.join(R, "study2", "conf2_scores.csv"))
G = e[(e.view == "global") & (e.group == "rare")].groupby(["ds", "k", "seed", "method"]).f1.mean().unstack("method")
O = e[e.view == "owner"].groupby(["ds", "k", "seed"]).f1.mean()
fig, axs = plt.subplots(1, 2, figsize=(6.3, 3.0))
for ax, ds in zip(axs, ["unsw", "ton"]):
    s = G.xs(ds, level="ds"); pk = lambda col: {k: s.xs(k, level="k")[col].values for k in [5, 20, 100]}
    series = [("Central-bal (pooled data)", pk("Central-bal argmax")), ("SAFE-X (ours)", pk("SAFE-X (Experts[fed] + GB+CR)")),
              ("FedOV-tab + OC", pk("FedOV+OC")), ("CCVR + OC", pk("CCVR+OC")),
              ("Owner's local model (own class)", {k: O.xs((ds, k)).values for k in [5, 20, 100]}),
              ("SAFE-X, owner-only calibration", pk("Experts[own] + GB+CR"))]
    panel(ax, series, DSN[ds]); ax.set_ylabel("Rare-class F1")
h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=3,fontsize=7)
fig.tight_layout(rect=(0,0.14,1,1)); fig.savefig(OUT + "/fig4_safex.pdf"); fig.savefig(OUT + "/fig4_safex.png", dpi=600); plt.close(fig)

# Fig 1 (overview) is drawn by make_fig1.py; the graphical abstract by make_graphical_abstract.py.

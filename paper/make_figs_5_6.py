"""Figs. 5-6: false alarms of the shared experts and SAFE-X vs the better calibrated FedOV, across Studies 2-4.
Values are the pre-registered outcomes in results/study2/conf2_report.md, results/study3/study3_report.md,
results/study4/study4_report.md and results/study4/s4_far.csv.  Usage: python3 figs_summary.py OUT_DIR"""
import sys, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "legend.frameon": False, "svg.fonttype": "none", "pdf.fonttype": 42, "ps.fonttype": 42})
BLUE, ORANGE, GREEN, GREY, INK, MUTE = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984", "#0b0b0b", "#52514e"
DSN = {"unsw": "NF-UNSW-NB15-v3", "ton": "NF-ToN-IoT-v3", "cic": "NF-CSE-CIC-IDS2018-v3"}

def save(fig, name):
    for ext in ("png", "pdf", "svg"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=600 if ext == "png" else None, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)

def grouped_rows(groups):
    """groups: [(dataset, [(label, payload), ...]), ...] -> y positions top-down with a gap between datasets."""
    rows, y, heads = [], 0.0, []
    for ds, items in groups:
        heads.append((ds, y)); y += 1.0
        for lab, pay in items: rows.append((y, lab, pay)); y += 1.0
        y += 0.5
    return rows, heads, y

# ---------- Fig. 5: false-alarm rate, owner-only vs federated calibration (percent of non-rare test flows)
FA = [("unsw", [("Study 2, Dirichlet, K = 10", (0.36, 0.15)), ("Study 4, K = 20", (0.340, 0.142)), ("Study 4, K = 50", (0.416, 0.144)),
                ("Study 4, 2 owners", (0.282, 0.133)), ("Study 4, 3 owners", (0.268, 0.127))]),
      ("ton",  [("Study 2, Dirichlet, K = 10", (0.60, 0.26)), ("Study 3, host-defined clients", (6.89, 0.18)), ("Study 4, K = 20", (0.693, 0.312)),
                ("Study 4, K = 50", (0.645, 0.269)), ("Study 4, 2 owners", (0.715, 0.295)), ("Study 4, 3 owners", (0.842, 0.380))]),
      ("cic",  [("Study 3, Dirichlet, K = 10", (5.15, 1.30)), ("Study 4, K = 20", (5.64, 1.44)), ("Study 4, K = 50", (4.51, 0.640)),
                ("Study 4, 2 owners", (5.51, 1.38)), ("Study 4, 3 owners", (4.73, 1.54))])]
rows, heads, H = grouped_rows(FA)
fig, ax = plt.subplots(figsize=(6.3, 4.0))
for y, lab, (own, fed) in rows:
    ax.annotate("", (fed, y), (own, y), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.0, shrinkA=4, shrinkB=4, mutation_scale=8))
    ax.plot(own, y, "o", ms=6, mfc="white", mec=ORANGE, mew=1.4, zorder=3)
    ax.plot(fed, y, "o", ms=6, color=BLUE, zorder=3)
    ax.text(13.5, y, f"{own / fed:.1f}×", va="center", ha="left", fontsize=7.5, color=INK)
ax.axvline(0.1, color=GREEN, lw=1.1, ls="--", zorder=1)
ax.text(0.1, -0.9, "target 0.1%", color=GREEN, ha="center", va="bottom", fontsize=7.5)
ax.set_yticks([y for y, _, _ in rows]); ax.set_yticklabels([lab for _, lab, _ in rows])
for ds, y in heads: ax.text(-0.012, y, DSN[ds], transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=8, fontweight="bold", color=INK)
ax.set_xscale("log"); ax.set_xlim(0.08, 12); ax.set_ylim(H - 0.3, -1.2)
ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10]); ax.set_xticklabels(["0.1%", "0.2%", "0.5%", "1%", "2%", "5%", "10%"]); ax.minorticks_off()
ax.set_xlabel("False-alarm rate of the shared experts on non-rare test flows (log scale)")
ax.grid(axis="x", color="#e6e5e0", lw=0.6); ax.tick_params(axis="y", length=0)
ax.text(13.5, -0.9, "reduction", ha="left", va="bottom", fontsize=7.5, color=MUTE)
h1, = ax.plot([], [], "o", ms=6, mfc="white", mec=ORANGE, mew=1.4, label="Owner-only calibration")
h2, = ax.plot([], [], "o", ms=6, color=BLUE, label="Federated calibration (SAFE-X)")
fig.legend(handles=[h1, h2], loc="lower center", ncol=2, bbox_to_anchor=(0.55, -0.01))
fig.tight_layout(rect=(0, 0.05, 1, 1)); save(fig, "fig5_falsealarms")

# ---------- Fig. 6: SAFE-X minus the better calibrated FedOV, rare-class F1 points with 95% CIs
FP = [("unsw", [("Study 2, Dirichlet, K = 10 *", (3.5, 2.5, 4.3)), ("Study 3, Dirichlet, K = 10", (3.5, 2.3, 4.7)), ("Study 4, K = 20", (2.7, 0.8, 4.6)),
                ("Study 4, K = 50", (-0.1, -3.4, 3.1)), ("Study 4, 2 owners", (6.2, 4.8, 7.4)), ("Study 4, 3 owners", (7.6, 6.3, 9.0))]),
      ("ton",  [("Study 2, Dirichlet, K = 10 *", (3.8, -0.6, 7.7)), ("Study 3, Dirichlet, K = 10", (0.2, -3.5, 3.6)), ("Study 3, host-defined clients", (3.6, 0.3, 6.9)),
                ("Study 4, K = 20", (-2.3, -8.2, 2.5)), ("Study 4, K = 50", (-2.3, -7.0, 2.2)), ("Study 4, 2 owners", (1.6, -1.7, 5.5)), ("Study 4, 3 owners", (3.4, 0.7, 6.4))]),
      ("cic",  [("Study 3, Dirichlet, K = 10", (4.1, 2.1, 5.8)), ("Study 4, K = 20", (7.5, 1.5, 13.1)), ("Study 4, K = 50", (6.5, 2.6, 10.1)),
                ("Study 4, 2 owners", (6.9, 1.2, 12.2)), ("Study 4, 3 owners", (6.4, 3.1, 9.8))])]
rows, heads, H = grouped_rows(FP)
fig, ax = plt.subplots(figsize=(6.3, 4.3))
ax.axvline(0, color=MUTE, lw=0.9, zorder=1)
for y, lab, (m, lo, hi) in rows:
    sig = lo > 0 or hi < 0
    col = BLUE if lo > 0 else (ORANGE if hi < 0 else GREY)
    ax.plot([lo, hi], [y, y], color=col, lw=1.6, solid_capstyle="butt", zorder=2)
    ax.plot(m, y, "D" if sig else "o", ms=5.5, color=col if sig else "white", mec=col, mew=1.3, zorder=3)
    ax.text(15.6, y, f"{m:+.1f} [{lo:+.1f}, {hi:+.1f}]".replace("-", "\u2212"), va="center", ha="left", fontsize=7.2, color=INK)
ax.set_yticks([y for y, _, _ in rows]); ax.set_yticklabels([lab for _, lab, _ in rows])
for ds, y in heads: ax.text(-0.012, y, DSN[ds], transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=8, fontweight="bold", color=INK)
ax.set_xlim(-9.5, 15); ax.set_ylim(H - 0.3, -1.2)
ax.set_xlabel("SAFE-X minus the better calibrated FedOV (rare-class F1 points, 95% CI)")
ax.grid(axis="x", color="#e6e5e0", lw=0.6); ax.tick_params(axis="y", length=0)
ax.text(15.6, -0.9, "difference [95% CI]", ha="left", va="bottom", fontsize=7.5, color=MUTE)
ax.text(-0.4, -0.9, "← FedOV better", ha="right", va="bottom", fontsize=7.5, color=MUTE)
ax.text(0.4, -0.9, "SAFE-X better →", ha="left", va="bottom", fontsize=7.5, color=MUTE)
h1, = ax.plot([], [], "D", ms=5.5, color=BLUE, label="CI above 0")
h2, = ax.plot([], [], "o", ms=5.5, color="white", mec=GREY, mew=1.3, label="CI includes 0")
fig.legend(handles=[h1, h2], loc="lower center", ncol=2, bbox_to_anchor=(0.55, -0.01))
fig.tight_layout(rect=(0, 0.05, 1, 1)); save(fig, "fig6_forest")
print("done")

import os, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans"})
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "fig1_overview.png")
INK, MUTE, LINE = "#0b0b0b", "#52514e", "#52514e"
RARE = ("#fdf0ea", "#eb6834"); COMM = ("#eef4fc", "#2a78d6"); CAL = ("#e8f6f0", "#1baf7a"); FUS = ("#f1effc", "#6250d6")
fig, ax = plt.subplots(figsize=(7.48, 3.3)); ax.set_xlim(0, 100); ax.set_ylim(0, 46); ax.axis("off")
W, H = 20, 13; X = [2, 29, 56]; XF = 83; WF = 16; YT, YB = 26, 2
def box(x, y, w, h, title, body, col):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=col[0], ec=col[1], lw=1.1))
    ax.text(x + w/2, y + h - 2.2, title, ha="center", va="center", fontsize=6.9, weight="bold", color=INK)
    ax.text(x + w/2, y + (h - 3.6)/2, body, ha="center", va="center", fontsize=6.2, color=INK, linespacing=1.35)
def arrow(pts, label=None, lx=None, ly=None, ha="center"):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1] + (xs[-1],), ys, color=LINE, lw=1.0, solid_capstyle="butt") if len(pts) > 2 else None
    ax.annotate("", pts[-1], pts[-2], arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.0, mutation_scale=9, shrinkA=0, shrinkB=0))
    if label: ax.text(lx, ly, label, ha=ha, va="bottom", fontsize=6.0, color=MUTE, style="italic")
# column headers
for x, w, t in [(X[0], W, "Data"), (X[1], W, "Training"), (X[2], W, "Calibration"), (XF, WF, "Inference")]:
    ax.text(x + w/2, 44, t, ha="center", va="center", fontsize=7.2, weight="bold", color=MUTE)
ax.plot([1, 99], [41.8, 41.8], color="#d9d8d3", lw=0.8)
ax.text(0.2, YT + H/2, "Rare class c", rotation=90, ha="right", va="center", fontsize=6.3, color=RARE[1], weight="bold")
ax.text(0.2, YB + H/2, "All classes", rotation=90, ha="right", va="center", fontsize=6.3, color=COMM[1], weight="bold")
box(X[0], YT, W, H, "Owner client j", "k labeled flows\nof rare class c", RARE)
box(X[1], YT, W, H, "(1) Local expert $f_c$", "class-balanced MLP,\ntrained only at\nthe owner", RARE)
box(X[2], YT, W, H, r"(3) Threshold $\tau_c$", r"$\tau_c$ = (1 − q) quantile" + "\n" + r"of $s_c$ over all clients'" + "\nnon-rare flows", CAL)
box(X[0], YB, W, H, "Clients 1, …, K", "benign and\ncommon-attack flows", COMM)
box(X[1], YB, W, H, "Global model g", "federated training\n(GB+CR)", COMM)
box(XF, YB, WF, YT + H - YB, "(4) Fusion", r"for each flow x:" + "\n\n" + r"if $s_c(x) \geq \tau_c$" + "\nfor some c:\npredict rare class c\n\notherwise:\nuse the prediction\nof g", FUS)
ym, yb = YT + H/2, YB + H/2
arrow([(X[0]+W, ym), (X[1], ym)])
arrow([(X[1]+W, ym), (X[2], ym)], "(2) share\nwith all", (X[1]+W+X[2])/2, ym + 0.6)
arrow([(X[2]+W, ym), (XF, ym)], r"$f_c$, $\tau_c$", (X[2]+W+XF)/2, ym + 0.6)
arrow([(X[0]+W, yb), (X[1], yb)])
arrow([(X[1]+W, yb), (XF, yb)], "g", (X[1]+W+XF)/2, yb + 0.6)
yc = 19.5
xs = X[0] + W/2; xe = X[2] + W/2
ax.plot([xs, xs, xe], [YB + H, yc, yc], color=LINE, lw=1.0)
ax.annotate("", (xe, YT), (xe, yc), arrowprops=dict(arrowstyle="-|>", color=LINE, lw=1.0, mutation_scale=9, shrinkA=0, shrinkB=0))
ax.text((xs + xe)/2, yc + 0.6, "histogram of $s_c$ on each client's own flows (secure aggregation)", ha="center", va="bottom", fontsize=6.0, color=MUTE, style="italic")
fig.savefig(OUT, dpi=300, bbox_inches="tight", pad_inches=0.04)

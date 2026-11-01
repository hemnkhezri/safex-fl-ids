"""Graphical abstract: problem -> SAFE-X -> results (numbers as in the abstract)."""
import os, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans", "pdf.fonttype": 42, "ps.fonttype": 42})
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "graphical_abstract")
INK, MUTE, GRID = "#0b0b0b", "#52514e", "#d9d8d3"
RARE = ("#fdf0ea", "#eb6834"); COMM = ("#eef4fc", "#2a78d6"); CAL = ("#e8f6f0", "#1baf7a"); FUS = ("#f1effc", "#6250d6")
fig, ax = plt.subplots(figsize=(7.5, 3.0)); ax.set_xlim(0, 150); ax.set_ylim(0, 60); ax.axis("off")
def panel(x, w, title, col):
    ax.add_patch(FancyBboxPatch((x, 2), w, 56, boxstyle="round,pad=0,rounding_size=2", fc="white", ec=col, lw=1.4))
    ax.add_patch(FancyBboxPatch((x, 50), w, 8, boxstyle="round,pad=0,rounding_size=2", fc=col, ec=col, lw=1.4))
    ax.text(x + w/2, 54, title, ha="center", va="center", fontsize=9.5, weight="bold", color="white")
def client(x, y, col, label=None, r=3.4):
    ax.add_patch(FancyBboxPatch((x - r, y - r), 2*r, 2*r, boxstyle="round,pad=0,rounding_size=0.9", fc=col[0], ec=col[1], lw=1.1))
    if label: ax.text(x, y, label, ha="center", va="center", fontsize=8, weight="bold", color=col[1])
def arrow(p0, p1, col=MUTE, lw=1.1):
    ax.annotate("", p1, p0, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=10, shrinkA=0, shrinkB=0))
GREY = ("#f3f2ef", "#9a9893")
# ---- panel 1: the problem
panel(2, 44, "The problem", RARE[1])
ax.text(24, 45, "a rare attack is labeled\nat one site only (5–100 flows)", ha="center", va="top", fontsize=7.6, color=INK, linespacing=1.3)
cx = [9, 18.5, 28, 37.5]
for i, x in enumerate(cx):
    client(x, 30, RARE if i == 0 else GREY, "!" if i == 0 else "?")
ax.text(9, 24.6, "owner", ha="center", va="top", fontsize=6.6, color=RARE[1], weight="bold")
ax.text(28, 24.6, "never saw it", ha="center", va="top", fontsize=6.6, color=MUTE)
ax.plot([15.5, 40.5], [25.2, 25.2], color=GRID, lw=0.8)
ax.text(24, 17.0, "Federated averaging\ndilutes it", ha="center", va="center", fontsize=7.6, color=INK, linespacing=1.3)
ax.text(24, 9.0, "−7 to −29 F1 points", ha="center", va="center", fontsize=10, weight="bold", color=RARE[1])
ax.text(24, 5.2, "vs pooled training", ha="center", va="center", fontsize=6.8, color=MUTE)
# ---- panel 2: SAFE-X
panel(53, 44, "SAFE-X", COMM[1])
client(62, 38, RARE, "!")
ax.text(62, 43.2, "owner", ha="center", va="bottom", fontsize=6.6, color=RARE[1], weight="bold")
ax.add_patch(FancyBboxPatch((72, 34), 20, 8, boxstyle="round,pad=0,rounding_size=1", fc=RARE[0], ec=RARE[1], lw=1.1))
ax.text(82, 38, "expert $f_c$", ha="center", va="center", fontsize=8, weight="bold", color=INK)
arrow((65.6, 38), (72, 38))
ax.text(75.5, 29.6, "(1) shared with all sites", ha="center", va="center", fontsize=6.6, color=MUTE, style="italic", zorder=5, bbox=dict(fc="white", ec="none", pad=0.6))
for x in (62, 71, 80, 89):
    client(x, 22, COMM, r=3.0)
    arrow((82, 33.6), (x, 25.3), col=GRID, lw=0.9)
ax.add_patch(FancyBboxPatch((56, 4.5), 38, 11, boxstyle="round,pad=0,rounding_size=1", fc=CAL[0], ec=CAL[1], lw=1.1))
ax.text(75, 12.6, "(2) federated calibration", ha="center", va="center", fontsize=7.2, weight="bold", color=INK)
ax.text(75, 7.9, r"threshold $\tau_c$ set on all sites'" + "\ntraffic, no raw flows shared", ha="center", va="center", fontsize=6.6, color=INK, linespacing=1.25)
for x in (62, 71, 80, 89):
    arrow((x, 18.8), (x, 15.1), col=CAL[1], lw=0.9)
# ---- panel 3: results
panel(104, 44, "Results", FUS[1])
ax.text(126, 45, "5 pre-registered studies,\n3 NetFlow v3 datasets", ha="center", va="top", fontsize=7.6, color=INK, linespacing=1.3)
def stat(y, big, small, col):
    ax.add_patch(FancyBboxPatch((108, y), 36, 12, boxstyle="round,pad=0,rounding_size=1", fc=col[0], ec=col[1], lw=1.0))
    ax.text(126, y + 8.8, big, ha="center", va="center", fontsize=10, weight="bold", color=col[1])
    ax.text(126, y + 3.6, small, ha="center", va="center", fontsize=6.6, color=INK, linespacing=1.15)
stat(25, "2.1–38× fewer", "false alarms than\nowner-only calibration", CAL)
stat(11, "12 of 18 settings", "SAFE-X beats calibrated\nFedOV in rare-attack F1", FUS)
ax.text(126, 6.6, "significantly behind in none", ha="center", va="center", fontsize=6.6, color=MUTE, style="italic")
for x0 in (46, 97):
    arrow((x0 + 0.8, 30), (x0 + 6.2, 30), col=INK, lw=1.6)
fig.savefig(OUT + ".pdf", bbox_inches="tight", pad_inches=0.04)
fig.savefig(OUT + ".png", dpi=400, bbox_inches="tight", pad_inches=0.04)

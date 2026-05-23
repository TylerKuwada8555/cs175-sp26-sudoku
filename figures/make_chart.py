"""
Generate the progress report's benchmark comparison chart.

Reads the numbers we got from running benchmarks/run_benchmark.py and
plots time + nodes side by side as bar charts on a log scale.
Saves to figures/benchmark_comparison.png.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Data from running benchmarks/run_benchmark.py
# format: (difficulty, plain_time, csp_time, plain_nodes, csp_nodes)
# None means "timed out / skipped"
data = [
    ("easy",     0.0064,    0.0024,    1526,      1),
    ("medium",   31.7272,   0.0014,    6546495,   0.5),   # 0.5 to be visible on log scale
    ("hard",     0.9045,    0.0403,    188453,    40),
    ("expert",   None,      1.1222,    None,      1090),
    ("17-clue",  None,      1.2725,    None,      1315),
]

difficulties = [d[0] for d in data]
plain_times = [d[1] if d[1] is not None else 30.0 for d in data]   # 30 = timeout threshold
csp_times = [d[2] for d in data]
plain_nodes = [d[3] if d[3] is not None else 1e7 for d in data]
csp_nodes = [d[4] for d in data]

# track which bars are timeouts (so we can hatch them)
plain_timeout = [d[1] is None for d in data]

x = np.arange(len(difficulties))
width = 0.38

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# --- Left subplot: solve time ---
bars1a = ax1.bar(x - width/2, plain_times, width,
                 label="Plain backtracking", color="#d62728")
bars1b = ax1.bar(x + width/2, csp_times, width,
                 label="Backtracking + AC-3 + MRV/LCV", color="#2ca02c")

# hatch timeouts
for bar, is_to in zip(bars1a, plain_timeout):
    if is_to:
        bar.set_hatch("///")
        bar.set_alpha(0.5)

ax1.set_yscale("log")
ax1.set_ylabel("Solve time (seconds, log scale)")
ax1.set_title("Solve time by difficulty")
ax1.set_xticks(x)
ax1.set_xticklabels(difficulties)
ax1.legend(loc="upper left")
ax1.grid(True, axis="y", linestyle="--", alpha=0.5)
ax1.axhline(y=30, color="gray", linestyle=":", linewidth=1)
ax1.text(0.02, 30 * 1.2, "30s timeout", color="gray", fontsize=9)

# label timeout bars
for i, is_to in enumerate(plain_timeout):
    if is_to:
        ax1.text(i - width/2, 30 * 1.05, "timeout", ha="center",
                 fontsize=8, color="#d62728", fontweight="bold")

# --- Right subplot: nodes expanded ---
bars2a = ax2.bar(x - width/2, plain_nodes, width,
                 label="Plain backtracking", color="#d62728")
bars2b = ax2.bar(x + width/2, csp_nodes, width,
                 label="Backtracking + AC-3 + MRV/LCV", color="#2ca02c")

for bar, is_to in zip(bars2a, plain_timeout):
    if is_to:
        bar.set_hatch("///")
        bar.set_alpha(0.5)

ax2.set_yscale("log")
ax2.set_ylabel("Search nodes expanded (log scale)")
ax2.set_title("Search effort by difficulty")
ax2.set_xticks(x)
ax2.set_xticklabels(difficulties)
ax2.legend(loc="upper left")
ax2.grid(True, axis="y", linestyle="--", alpha=0.5)

for i, is_to in enumerate(plain_timeout):
    if is_to:
        ax2.text(i - width/2, 1e7 * 1.2, "timeout", ha="center",
                 fontsize=8, color="#d62728", fontweight="bold")

fig.suptitle(
    "Plain backtracking vs. CSP (AC-3 + MRV + LCV) on the puzzle bank",
    fontsize=13, fontweight="bold"
)
fig.tight_layout(rect=[0, 0, 1, 0.96])

os.makedirs("figures", exist_ok=True)
out = "figures/benchmark_comparison.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved to {out}")

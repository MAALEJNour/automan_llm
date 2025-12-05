import os

import matplotlib.pyplot as plt
import numpy as np
SAVE_DIR = "plots"
os.makedirs(SAVE_DIR, exist_ok=True)
# ----------------------------------------
# Speed-up values you computed
# ----------------------------------------
speedups = {
    "SC1": 4.36,
    "SC2": 3.57,
    "SC3": 1.12
}

scenarios = list(speedups.keys())
values = list(speedups.values())

# ----------------------------------------
# Plot
# ----------------------------------------
plt.figure(figsize=(10, 6))

bars = plt.bar(scenarios, values)


# Add value labels on top
for i, v in enumerate(values):
    plt.text(i, v + 0.1, f"{v:.2f}×", ha="center", fontsize=12, fontweight="bold")

plt.title("Speed-Up Comparison: Gemini-2.5-pro vs DeepSeek", fontsize=16, fontweight="bold")
plt.ylabel("Speed-Up Factor (×)")
plt.ylim(0, max(values) + 1)

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
out_path = os.path.join(SAVE_DIR, "speedup_comparison.png")
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()
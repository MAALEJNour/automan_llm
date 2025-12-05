# charts.py
import matplotlib.colors as mcolors
from matplotlib import colormaps, animation
from matplotlib.animation import FFMpegWriter

from data_loader import *
import math
import os
import numpy as np
import matplotlib.pyplot as plt

SAVE_DIR = "plots"
os.makedirs(SAVE_DIR, exist_ok=True)
# --- NEW helpers (add these) ---
def _iter_result_files(root_dir: str):
    """Yield full paths to *_results.json recursively under root_dir."""
    for dirpath, _, files in os.walk(root_dir):
        for fn in files:
            if fn.endswith("_results.json"):
                yield os.path.join(dirpath, fn)

def _extract_latencies_from_json(fp: str):
    """Return (model, series:list[float]) from a single results.json with multiple key fallbacks."""
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)

    model = data.get("model", os.path.splitext(os.path.basename(fp))[0])

    series = []
    for key in ("total_latency"):
        vals = data.get(key)
        if isinstance(vals, list):
            series.extend(
                float(x)
                for x in vals
                if isinstance(x, (int, float)) and not math.isnan(x)
            )

    return model, series
def latency_bar_chart_animated(scenario_label: str, provider: str | None = None) -> str:
    data = collect_avg_latencies(scenario_label, provider=provider)
    if not data:
        raise RuntimeError(f"No latency data for {scenario_label}")

    models = [d.model for d in data]
    avgs   = [d.avg_latency for d in data]

    # Normalize colors as before
    norm = mcolors.Normalize(vmin=min(avgs), vmax=max(avgs))
    cmap = colormaps["RdYlGn_r"]
    colors = cmap(norm(avgs))

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("white")

    bars = ax.barh(models, np.zeros_like(avgs), color=colors)
    ax.set_xlim(0, max(avgs) * 1.1)

    ax.set_title(f"Average Total Latency — {scenario_label}", fontsize=15, fontweight="bold")
    ax.set_xlabel("Latency (seconds)")
    ax.set_ylabel("Model")

    # Animation function
    def animate(frame):
        progress = frame / 100  # 0 → 1
        for bar, target in zip(bars,  avgs):
            bar.set_width(target * progress)
        return bars

    anim = animation.FuncAnimation(fig, animate, frames=100, interval=20, blit=False)

    out_path = os.path.join(SAVE_DIR, f"latency_comparison_{scenario_label}_animated.mp4")
    writer = FFMpegWriter (fps=30, bitrate=3000,
    extra_args=["-preset", "fast"] )
    anim.save (out_path, writer=writer)
    plt.close(fig)
    return out_path
def accuracy_bar_chart_from_scores(
    scenario_label: str,
    prompt_type: str,
    provider_type: str,
    show: bool = True
) -> str:

    # ----- Validate mandatory arguments -----
    valid_prompt_types = {"action_plan", "contact_plan"}
    valid_providers = {"local", "cloud"}

    if prompt_type not in valid_prompt_types:
        raise ValueError(
            f"Invalid prompt_type '{prompt_type}'. "
            f"Expected one of: {valid_prompt_types}"
        )

    if provider_type not in valid_providers:
        raise ValueError(
            f"Invalid provider '{provider_type}'. "
            f"Expected one of: {valid_providers}"
        )

    # ----- NEW directory structure -----
    base_dir = os.path.join("scores", prompt_type, scenario_label, provider_type)

    if not os.path.isdir(base_dir):
        raise FileNotFoundError(
            f"Expected directory not found: '{base_dir}'\n"
            f"Structure must be: scores/<prompt_type>/<scenario>/<provider>/"
        )

    # ----- Load accuracy scores -----
    data = collect_scores(
        scenario_label=scenario_label,
        plan_type=prompt_type,
        provider_type=provider_type,
        root="scores",
    )

    if not data:
        raise RuntimeError(
            f"No scores found for scenario={scenario_label}, "
            f"prompt={prompt_type}, provider={provider_type}"
        )

    models = [d.model for d in data]
    scores = [d.score for d in data]

    # ----- Colors -----
    norm = mcolors.Normalize(vmin=min(scores) - 0.5, vmax=max(scores) + 0.5)
    cmap = colormaps["RdYlGn"]
    colors = cmap(norm(scores))

    # ----- Plot -----
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("white")
    ax.barh(models, scores, color=colors)

    title = (
      "Model Scores"
    )

    ax.set_title(title, fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Score (1–10)")
    ax.set_ylabel("Model")
    ax.set_xticks([1,2,3,4,5,6,7,8,9,10])

    # Text labels
    bump = 0.02 * max(scores)
    for i, v in enumerate(scores):
        ax.text(v + bump, i, f"{v:.1f}/10", va="center", fontsize=10)

    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax).set_label("Accuracy Gradient (Red = Low, Green = High)")

    # Save
    out_path = os.path.join(
        SAVE_DIR,
        f"model_scores_{scenario_label}_{prompt_type}_{provider_type}.png"
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", pad_inches=0.2)

    if show:
        plt.show()

    return out_path
# -------- Smoothed latency plot using the loader above --------
def plot_all_latency_smoothed(
    scenario_label: str,
    provider: str | None = None,
    rolling_window: int = 5,
    ylim: tuple[float, float] | None = None,
    show: bool = True,
) -> str:
    """
    Plot smoothed latency curves for all models in a scenario/provider.

    - Reads standardized results via collect_latency_series()
    - Applies a rolling mean with window=min(rolling_window, len(series))
    - Saves to plots/latency_smoothed_<scenario>[_<provider>].png
    - Returns the output path
    """
    series = collect_latency_series(scenario_label, provider)
    if not series or all(len(v) == 0 for v in series.values()):
        scan_hint = f"{scenario_label}" + (f"/{provider}" if provider else "")
        raise RuntimeError(f"No latency series found for '{scan_hint}'.")

    # Sort models by average latency (ascending) for nicer legend ordering
    def _avg(xs: list[float]) -> float:
        return float(np.mean(xs)) if xs else float("inf")
    sorted_items = sorted(series.items(), key=lambda kv: _avg(kv[1]))

    plt.figure(figsize=(12, 7))

    def _roll_mean(arr: list[float], window: int) -> np.ndarray:
        if not arr:
            return np.array([])
        w = max(1, min(window, len(arr)))
        if w == 1:
            return np.asarray(arr, dtype=float)
        kernel = np.ones(w) / w
        return np.convolve(np.asarray(arr, dtype=float), kernel, mode="valid")

    for model, vals in sorted_items:
        if not vals:
            continue
        roll = _roll_mean(vals, rolling_window)
        if roll.size == 0:
            continue

        # X axis alignment: when w==1 → 1..N, else valid window positions w..N
        w = max(1, min(rolling_window, len(vals)))
        x = np.arange(w, len(vals) + 1) if w > 1 else np.arange(1, len(vals) + 1)

        plt.plot(x, roll, linewidth=2.0, label=f"{model} (n={len(vals)})")

    title = f"Model Latency Trends: {scenario_label}" + (f" — {provider}" if provider else "")
    plt.title(title)
    plt.xlabel("Trial number")
    plt.ylabel("Total latency (s)")
    if ylim:
        plt.ylim(ylim)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0.0)
    plt.tight_layout()

    os.makedirs(SAVE_DIR, exist_ok=True)
    fname = f"latency_smoothed_{scenario_label}" + (f"_{provider}" if provider else "") + ".png"
    out_path = os.path.join(SAVE_DIR, fname)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()

    return out_path

if __name__ == "__main__":
    # examples
  #  latency_bar_chart_animated("SCENARIO_1", provider="cloud")
    accuracy_bar_chart_from_scores ("SCENARIO_3", "contact_plan", "cloud")
  #  plot_all_latency_smoothed("SCENARIO_1", provider="local", rolling_window=0)
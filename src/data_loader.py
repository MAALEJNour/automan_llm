# data_loader.py
from __future__ import annotations
import os, json
from dataclasses import dataclass
from typing import List, Dict
import statistics as stats
import logging

# -----------------------------
# Logging setup (module-level)
# -----------------------------
logger = logging.getLogger("data_loader")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)

BENCH_ROOT = "benchmarking"
SCORE_ROOT = "scores"
os.makedirs(BENCH_ROOT, exist_ok=True)
os.makedirs(SCORE_ROOT, exist_ok=True)


@dataclass(frozen=True)
class ModelLatency:
    model: str
    avg_latency: float


@dataclass(frozen=True)
class ModelScore:
    model: str
    score: float


def collect_latency_series(
    plan_type: str,
    scenario_label: str,
    provider_type: str,
    provider: str,
    root: str = BENCH_ROOT,
) -> Dict[str, List[float]]:
    """
    Recursively scan benchmarking/<plan_type>/<scenario_label>/<provider_type>/<provider>/**/_results.json
    and return { model: [lat1, lat2, ...] }.
    Assumes standardized schema with key: total_latency.
    """
    scan_dir = os.path.join(root, plan_type, scenario_label, provider_type, provider)
    if not os.path.isdir(scan_dir):
        logger.info(
            "Latency directory '%s' does not exist (plan_type=%s, scenario=%s, provider_type=%s, provider=%s).",
            scan_dir, plan_type, scenario_label, provider_type, provider
        )
        return {}

    merged: Dict[str, List[float]] = {}

    for dirpath, _, files in os.walk(scan_dir):
        for fn in files:
            if not fn.endswith("_results.json"):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                logger.warning("Failed to read JSON file '%s': %s", fp, e)
                continue

            model = data.get("model", os.path.splitext(fn)[0])

            vals = data.get("total_latency", [])
            if not isinstance(vals, list):
                logger.warning(
                    "File '%s' has non-list 'total_latency' (%s). Skipping.",
                    fp, type(vals).__name__
                )
                continue

            numeric = []
            for x in vals:
                if isinstance(x, (int, float)):
                    numeric.append(float(x))
                else:
                    logger.warning(
                        "Non-numeric latency value in '%s' for model '%s': %r (ignored)",
                        fp, model, x
                    )
            if not numeric:
                logger.warning(
                    "No numeric latencies found in '%s' for model '%s'. Skipping.",
                    fp, model
                )
                continue

            merged.setdefault(model, []).extend(numeric)

    if not merged:
        logger.info(
            "No latency series found under '%s' (plan_type=%s, scenario=%s, provider_type=%s, provider=%s).",
            scan_dir, plan_type, scenario_label, provider_type, provider
        )
    return merged


def collect_avg_latencies(
    plan_type: str,
    scenario_label: str,
    provider_type: str,
    provider: str,
    root: str = BENCH_ROOT,
) -> List[ModelLatency]:
    """
    Average the standardized total_latency series per model.
    If multiple files for the same model exist, keep the lowest avg.
    """
    series = collect_latency_series(plan_type, scenario_label, provider_type, provider, root)
    best: dict[str, float] = {}
    for model, vals in series.items():
        if not vals:
            logger.warning("Empty latency list for model '%s' (plan_type=%s, scenario=%s, provider_type=%s, provider=%s).",
                           model, plan_type, scenario_label, provider_type, provider)
            continue
        try:
            avg = float(stats.fmean(vals))
        except Exception as e:
            logger.warning("Failed to compute mean for model '%s': %s", model, e)
            continue
        if model not in best or avg < best[model]:
            best[model] = avg
    if not best:
        logger.info("No averaged latencies produced (plan_type=%s, scenario=%s, provider_type=%s, provider=%s).",
                    plan_type, scenario_label, provider_type, provider)
    return [ModelLatency(m, v) for m, v in sorted(best.items(), key=lambda x: x[1])]

def collect_scores(
    plan_type: str,
    scenario_label: str,
    provider_type: str,
    root: str = SCORE_ROOT,
) -> List[ModelScore]:
    """
    Recursively scan:
        scores/<plan_type>/<scenario_label>/<provider_type>/<provider>/**/*.json

    Returns a de-duplicated list of ModelScore(model, score):
    - Keeps only highest score per model
    - Sorted ascending by score (for alignment with latency plots)
    """

    # Correct folder structure
    scan_dir = os.path.join(root, plan_type, scenario_label, provider_type)

    if not os.path.isdir(scan_dir):
        logger.info(
            "Score directory '%s' does not exist "
            "(plan_type=%s, scenario=%s, provider_type=%s, provider=%s).",
            scan_dir, plan_type, scenario_label, provider_type
        )
        return []

    rows: list[ModelScore] = []

    # Walk recursively through directory
    for dirpath, _, files in os.walk(scan_dir):
        for fn in files:
            if not fn.endswith(".json"):
                continue

            fp = os.path.join(dirpath, fn)

            try:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                logger.warning("Failed to read score JSON '%s': %s", fp, e)
                continue

            # Extract fields
            model = data.get("model") or os.path.splitext(fn)[0].replace("_score", "")
            score = data.get("score")

            if not isinstance(score, (int, float)):
                logger.warning(
                    "Score in '%s' for model '%s' is not numeric (%r). Skipping.",
                    fp, model, score
                )
                continue

            rows.append(ModelScore(model=model, score=score))

    if not rows:
        logger.info(
            "No score files found under '%s' "
            "(plan_type=%s, scenario=%s, provider_type=%s, provider=%s).",
            scan_dir, plan_type, scenario_label, provider_type
        )

    # De-duplicate: keep highest score for each model
    best: dict[str, float] = {}
    for entry in rows:
        if entry.model not in best or entry.score > best[entry.model]:
            best[entry.model] = entry.score

    # Return sorted list
    return [
        ModelScore(model, score)
        for model, score in sorted(best.items(), key=lambda x: x[1])
    ]
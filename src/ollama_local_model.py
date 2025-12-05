from typing import List, Dict, Tuple
import time
import ollama
from ollama import chat
from Prompts import *
from bench_io import save_content, save_results


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

N_WARM_TRIALS = 1
KEEP_ALIVE_WARM = "1h"
OPTIONS = {"temperature": 0, "seed": 42}  # more deterministic output

MODELS = [
    # "mistral",
    # "gemma3",
    "ministral-3:8b",
    # "llama3.1:8b",
    # "qwen3"
]

SCENARIOS = [
    ("SCENARIO_1", SCENARIO_1),
    ("SCENARIO_2", SCENARIO_2),
    ("SCENARIO_3", SCENARIO_3),
]

plan_type = "action_plan"
provider_type = "local"
provider = "ollama"


# -------------------------------------------------------------------
# Core inference function
# -------------------------------------------------------------------

def run_once(model: str, prompt: str, keep_alive: str | None = None) -> Tuple[float, str | None]:
    """
    Executes a synchronous model inference and returns:
        (total_latency_in_seconds, output_text or None)

    This version assumes that the model has already been pulled
    (e.g., via scripts/pull_models.sh). If the model is missing, or
    any error occurs, it prints an error and returns (NaN, None).
    """
    start_time = time.time()

    try:
        response = chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            keep_alive=keep_alive,
            options=OPTIONS,
            # think=True,  # only qwen3 supports thinking
        )
        output_text = response["message"]["content"]

    except ollama.ResponseError as e:
        # No automatic pulling here anymore: report the issue.
        print(f"[{model}] Ollama ResponseError (status {e.status_code}): {e.error}")
        print("Hint: Make sure this model is installed, e.g. via scripts/pull_models.sh")
        return float("nan"), None

    except Exception as e:
        # Non-Ollama unexpected error
        print(f"[{model}] Unexpected error: {e}")
        return float("nan"), None

    end_time = time.time()
    total_time = end_time - start_time
    return total_time, output_text


# -------------------------------------------------------------------
# Trials runner
# -------------------------------------------------------------------

def run_trials(
    model: str,
    trials: int,
    prompt: str,
    scenario_name: str,
    provider: str,
    plan_type: str,
) -> List[float]:
    """
    Runs N trials and measures latency.
    Saves the model output only ONCE per model (on the first successful run).
    """
    latencies: List[float] = []
    saved_once = False

    for _ in range(trials):
        total_time, output_text = run_once(
            model=model,
            prompt=prompt,
            keep_alive=KEEP_ALIVE_WARM,
        )

        latencies.append(total_time)

        # Save output only on the FIRST successful run with non-empty output
        if not saved_once and isinstance(output_text, str) and output_text.strip():
            save_content(
                plan_type=plan_type,
                provider=provider,
                provider_type=provider_type,
                prompt=prompt,
                content=output_text,
                scenario_name=scenario_name,
                model=model,
            )
            saved_once = True

    return latencies


# -------------------------------------------------------------------
# Main runner
# -------------------------------------------------------------------

def main() -> None:
    for scenario_name, scenario_prompt in SCENARIOS:
        print(f"\n=== Running {scenario_name} ===\n")

        results_for_scenario: Dict[str, List[float]] = {}

        for model in MODELS:
            latencies = run_trials(
                model=model,
                trials=N_WARM_TRIALS,
                prompt=scenario_prompt,
                scenario_name=scenario_name,
                provider=provider,
                plan_type="action_plan",
            )

            results_for_scenario[model] = latencies

            save_results(
                plan_type=plan_type,
                provider_type=provider_type,
                provider=provider,
                model=model,
                total_latency=latencies,
                scenario_name=scenario_name,
            )


if __name__ == "__main__":
    main()
from typing import List, Dict, Tuple
import time
import ollama
from ollama import chat
from Prompts import *
from bench_io import save_content, save_results


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

N_WARM_TRIALS = 100
KEEP_ALIVE_WARM = "12h"
OPTIONS = {"temperature": 0, "seed": 42}  # more deterministic output
scenario_name1= "SCENARIO_1"
scenario_name2= "SCENARIO_2"
scenario_name3= "SCENARIO_3"
scenario_name_SCENARIO_CLEANING_HOME= "SCENARIO_CLEANING_HOME"
scenario_name_SCENARIO_MAKING_COFFEE= "SCENARIO_MAKING_COFFEE"

#prompt= SCENARIO_3
# choose the scenario between 1 and 6
UNIFIED_PROMPT1= build_unified_prompt(scenario_name1)
UNIFIED_PROMPT2= build_unified_prompt(scenario_name2)
UNIFIED_PROMPT3= build_unified_prompt(scenario_name3)
UNIFIED_PROMPT_SCENARIO_CLEANING_HOME = build_unified_prompt(scenario_name_SCENARIO_CLEANING_HOME)
UNIFIED_PROMPT_SCENARIO_MAKING_COFFEE = build_unified_prompt(scenario_name_SCENARIO_MAKING_COFFEE)
MODELS = [
    # "mistral",
    # "gemma3",
  #  "qwen3:32b",
   # "gpt-oss:20b",
  #  "gemma3:27b",
    "phi4:14b",
    #"deepseek-r1:32b",
    #  "ministral-3:8b",
    # "llama3.1:8b",
    # "qwen3"
]

SCENARIOS = [
  #("SCENARIO_1", UNIFIED_PROMPT1),  
  #("SCENARIO_2", UNIFIED_PROMPT2),
  #("SCENARIO_3", UNIFIED_PROMPT3),

    ("SCENARIO_1", SCENARIO_1),
    ("SCENARIO_2", SCENARIO_2),
    ("SCENARIO_3", SCENARIO_3),
    ("SCENARIO_CLEANING_HOME",  SCENARIO_CLEANING_HOME),
    ("SCENARIO_MAKING_COFFEE",  SCENARIO_MAKING_COFFEE),

]

#plan_type = "action+contact_plan"
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

    print(f"[START] Scenario={scenario_name} | Model={model} | Trials={trials}")

    for trial_idx in range(1, trials + 1):
        print(f"[RUN] Scenario={scenario_name} | Model={model} | Trial {trial_idx}/{trials}")

        total_time, output_text = run_once(
            model=model,
            prompt=prompt,
            keep_alive=KEEP_ALIVE_WARM,
        )

        if total_time != total_time:  # NaN check
            print(f"[ERROR] Model={model} | Trial {trial_idx} returned NaN latency")
        else:
            print(f"[DONE] Model={model} | Trial {trial_idx} | Latency={total_time:.3f}s")

        latencies.append(total_time)

     #   if (
     ##       not saved_once
      #      and isinstance(output_text, str)
      #      and output_text.strip()
      #  ):
      #      print(f"[SAVE] Saving first output for Model={model} | Scenario={scenario_name}")

      #      save_content(
      #          plan_type=plan_type,
      #          provider=provider,
      #          provider_type=provider_type,
      #          prompt=prompt,
      #          content=output_text,
      #          scenario_name=scenario_name,
      #          model=model,
      #      )
      #      saved_once = True

    print(f"[END] Scenario={scenario_name} | Model={model}")

    return latencies



# -------------------------------------------------------------------
# Main runner
# -------------------------------------------------------------------
def main() -> None:
    print("\n===== BENCHMARK STARTED =====\n")

    for scenario_name, scenario_prompt in SCENARIOS:
        print(f"\n=== SCENARIO START: {scenario_name} ===\n")

        results_for_scenario: Dict[str, List[float]] = {}

        for model in MODELS:
            print(f"\n>>> Running Model: {model} on Scenario: {scenario_name}\n")

            latencies = run_trials(
                model=model,
                trials=N_WARM_TRIALS,
                prompt=scenario_prompt,
                scenario_name=scenario_name,
                provider=provider,
                plan_type=plan_type,
            )

            results_for_scenario[model] = latencies

            print(f"[RESULTS] Model={model} | Scenario={scenario_name} | Latencies={latencies}")

            save_results(
                plan_type=plan_type,
                provider_type=provider_type,
                provider=provider,
                model=model,
                total_latency=latencies,
                scenario_name=scenario_name,
            )

        print(f"\n=== SCENARIO END: {scenario_name} ===\n")

    print("\n===== BENCHMARK FINISHED =====\n")

if __name__ == "__main__":
    main()
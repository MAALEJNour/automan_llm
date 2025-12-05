from Prompts import *
from typing import Dict, List
from bench_io import save_results
from run_model import run_n_trials

# -----------------------------
# Config
# -----------------------------
N_TRIALS = 5  # warm runs
scenario_name= "SCENARIO_1"
#prompt= SCENARIO_3
# choose the scenario between 1 and 6
UNIFIED_PROMPT = build_unified_prompt(scenario_name)
# Models to benchmark
#MODEL1 = "gemini-2.5-pro" # most advanced model
MODEL1 = "gemini-3-pro" # most advanced model
MODEL2 = "gemini-2.5-flash-lite"# fastest model
MODEL3 = "gemini-2.0-flash" # second_generation, robust
MODEL4 = "gemini-robotics-er-1.5-preview" # special for robotic
MODELS = [MODEL1]
provider_type = "cloud"
provider="gemini"
plan_type= "action+contact_plan"
# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":


    print(f"Benchmarking {len(MODELS)} Gemini models (cloud latency test).")
    total_latency: Dict[str, List[float]] = {}

    for model in MODELS:
        print(f"\n=== {model} ===")
        # Warm phase
        results = run_n_trials(model, N_TRIALS,UNIFIED_PROMPT,scenario_name, provider= provider, provider_type= provider_type, plan_type= plan_type)
        total_latency[model] = results
        save_results(
            plan_type= plan_type,
            provider_type=provider_type,
            provider=provider,
            model=model,
            total_latency=total_latency[model],
            scenario_name=scenario_name,
        )

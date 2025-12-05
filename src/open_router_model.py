from bench_io import save_results
from Prompts import *
from run_model import run_n_trials

# -----------------------------
# Config
# -----------------------------
N_TRIALS = 1

# Models to benchmark (models available in OpenRouter)
MODEL1="deepseek/deepseek-r1-distill-llama-70b:free"
MODEL2="nvidia/nemotron-nano-12b-v2-vl:free"
MODEL3="perplexity/sonar-pro-search"
provider_type="cloud"
provider = "openrouter"
plan_type = "action_plan"
MODELS = [MODEL1]
# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    scenario_name = "SCENARIO_4"
    #unified= "unified_prompt_" + scenario_name
    #UNIFIED_PROMPT = build_unified_prompt_scenario_only(scenario_name)
    print(f"Benchmarking {len(MODELS)} OpenRouter models (cloud latency test).")

    for model in MODELS:
        print(f"\n=== {model} ===")
        results = run_n_trials(model, N_TRIALS,SCENARIO_4,scenario_name, provider = provider , plan_type = plan_type, provider_type = provider_type)

        # Save results
        save_results(
            plan_type= plan_type,
            provider= provider,
            provider_type=provider_type,
            model=model,
            total_latency=results,
            scenario_name=scenario_name,
        )



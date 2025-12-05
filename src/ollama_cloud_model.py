from run_model import run_n_trials
from bench_io import save_results
from Prompts import *


# models supported by ollama in the cloud
MODELS = ["glm-4.6:cloud",
         # "qwen3-vl:235b-cloud","deepseek-v3.1:671b-cloud","gpt-oss:20b-cloud",
         # "gpt-oss:120b-cloud"
          ]

N_TRIALS = 4
plan_type = "action+contact_plan"
provider = "ollama"
provider_type="cloud"
scenario_name = "SCENARIO_1"
#prompt= SCENARIO_1
UNIFIED_PROMPT = build_unified_prompt(scenario_name)

if __name__ == "__main__":

   # UNIFIED_PROMPT= build_unified_prompt_scenario_only(scenario_name)
   # task = "unified_prompt_" + scenario_name
    print("Benchmarking Ollama Cloud Models...\n")

    for model in MODELS:
        print(f"\n=== {model} ===")
        results = run_n_trials(model, N_TRIALS, UNIFIED_PROMPT,scenario_name,provider= provider, plan_type= plan_type, provider_type= provider_type)

        save_results(
            plan_type= plan_type,
            provider=provider,
            model=model,
            provider_type=provider_type,
            total_latency=results,
            scenario_name=scenario_name,
        )

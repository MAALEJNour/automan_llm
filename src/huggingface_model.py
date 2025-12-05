import asyncio
from typing import Dict, List
from bench_io import save_results
from Prompts import *
from run_model import run_n_trials

# -----------------------------
# Config
# -----------------------------
N_WARM_TRIALS = 1
MODELS = [
    "deepseek-ai/DeepSeek-V3.2-Exp",
]
provider_type = "cloud"
provider="huggingface"
plan_type= "action_plan"
prompt= SCENARIO_3
scenario_name= "SCENARIO_3"
# -----------------------------
# Main (async)
# ----------------------------
async def main():
    print(f"Benchmarking {len(MODELS)} HuggingFace models...\n")


    warm_total: Dict[str, List[float]] = {}

    for model in MODELS:
        print(f"\n=== {model} ===")
        warm_results = await run_n_trials(model, N_WARM_TRIALS, prompt,model,provider, provider_type= provider_type, plan_type= plan_type)
        warm_total[model] = warm_results
        save_results (
            plan_type=plan_type,
            provider_type=provider_type,
            provider=provider,
            model=model,
            total_latency=warm_total[model],
            scenario_name=scenario_name,
        )

if __name__ == "__main__":
    asyncio.run(main())

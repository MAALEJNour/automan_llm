import time
from typing import List
import os
import json


SAVE_LATENCY_DIR = "benchmarking"
os.makedirs(SAVE_LATENCY_DIR, exist_ok=True)

SAVE_CONTENT_DIR = "outputs"
os.makedirs(SAVE_CONTENT_DIR, exist_ok=True)

def save_results(
    plan_type: str,
    provider_type: str,
    provider: str,
    model: str,
    total_latency: List[float],
    scenario_name: str | int,
) -> None:
    """
    Save latency results under:
        benchmarking/<plan_type>/<scenario>/<provider_type>/<provider>/<model>_results.json
    """

    scenario_name = str(scenario_name)
    plan_type = plan_type.strip().lower().replace(" ", "_")

    safe_model = model.replace("/", "_").replace(":", "_")

    dir_path = os.path.join(
        SAVE_LATENCY_DIR,       # benchmarking/
        plan_type,              # action_plan / contact_plan / action+contact_plan
        scenario_name,          # SCENARIO_2
        provider_type,          # cloud / local / etc
        provider                # openrouter / ollama / etc
    )
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, f"{safe_model}_results.json")

    # Load or initialize structure
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                results = json.load(f)
        except Exception:
            results = {}
    else:
        results = {}

    results.setdefault("plan_type", plan_type)
    results.setdefault("provider", provider)
    results.setdefault("model", model)
    results.setdefault("total_latency", [])

    # Append new latency values
    results["total_latency"].extend(total_latency)

    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)



def save_content(
    plan_type: str,
    provider_type: str,
    provider: str,
    prompt: str,
    content: str,
    model: str,
    scenario_name: str | int,
) -> None:
    """
    Save output under:
        outputs/<plan_type>/<scenario>/<provider_type>/<provider>/<model>_output.txt
    """

    scenario_name = str(scenario_name)
    plan_type = plan_type.strip().lower().replace(" ", "_")
    safe_model = model.replace("/", "_").replace(":", "_")

    dir_path = os.path.join(
        SAVE_CONTENT_DIR,     # outputs/
        plan_type,            # action_plan / contact_plan / action+contact_plan
        scenario_name,        # SCENARIO_2
        provider_type,        # cloud / local / etc
        provider              # openrouter / ollama / etc
    )
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, f"{safe_model}_output.txt")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Prompt:\n{prompt}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Output:\n{content}\n")
        f.write("=" * 60 + "\n\n")
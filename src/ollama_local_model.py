from typing import List, Dict, Tuple
import time
from ollama import chat
from Prompts import *
from bench_io import *
import os
import re
import json
from baseline_output import  *
def build_contact_prompt(baseline_coordinator_output: str) -> str:
    return f"""
You are a helpful assistant in analyzing human-object interactions.

Each message describes one or more specific human-object interactions
that occur during a robot manipulation sequence.

You will receive MULTIPLE JSON inputs from the CoordinatorAgent.
Each JSON object describes ONE interaction step.

Your task:
- Process EACH input individually
- Generate ONE contact graph per interaction
- Return a LIST of JSON contact graphs
- Preserve the SAME ORDER as the inputs

Rules:
- Do NOT invent new actions
- Do NOT modify interaction descriptions
- Use only the provided interaction information
- Each output must be valid JSON

After you finish processing all inputs, write EXACTLY:
ALL INTERACTIONS PROCESSED

====================
INPUT INTERACTIONS:
{baseline_coordinator_output}
====================
"""
# -------------------------------------------------------------------
# Output comparison helpers
# -------------------------------------------------------------------
def _counts_file_path(
    plan_type: str,
    scenario_name: str,
    provider_type: str,
    provider: str,
    model: str,
) -> str:
    plan_type = plan_type.strip().lower().replace(" ", "_")
    scenario_name = str(scenario_name)
    safe_model = model.replace("/", "_").replace(":", "_")

    return os.path.join(
        SAVE_CONTENT_DIR,
        plan_type,
        scenario_name,
        provider_type,
        provider,
        f"{safe_model}_counts.json",
    )


def _load_output_counts(path: str) -> Dict[str, int]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_output_counts(path: str, counts: Dict[str, int]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)


def _normalize_text(text: str) -> str:
    """
    Normalize model output to allow robust comparison:
    - lowercase
    - strip whitespace
    - remove numbering like '1.' '2.' etc
    - collapse multiple spaces
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()

    # remove numbered list prefixes: "1. ", "2) ", etc.
    text = re.sub(r"^\s*\d+[\.\)]\s*", "", text, flags=re.MULTILINE)

    # collapse whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def _existing_outputs_for_model(
    plan_type: str,
    scenario_name: str,
    provider_type: str,
    provider: str,
    model: str,
) -> List[str]:
    """
    Read all previously saved outputs for a given (model, scenario).
    Returns a list of raw output strings.
    """
    plan_type = plan_type.strip().lower().replace(" ", "_")
    scenario_name = str(scenario_name)
    safe_model = model.replace("/", "_").replace(":", "_")

    file_path = os.path.join(
        SAVE_CONTENT_DIR,
        plan_type,
        scenario_name,
        provider_type,
        provider,
        f"{safe_model}_output.txt",
    )

    if not os.path.exists(file_path):
        return []

    outputs: List[str] = []
    current_block: List[str] = []
    recording = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Output:"):
                recording = True
                current_block = []
                continue
            if recording and line.startswith("=" * 60):
                outputs.append("".join(current_block).strip())
                recording = False
                continue
            if recording:
                current_block.append(line)

    return outputs
# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

N_WARM_TRIALS = 10
KEEP_ALIVE_WARM =None # KEEP_ALIVE_WARM ow long the model stays in memory after a request 
OPTIONS = {"temperature": 0, "seed": 42}  # more deterministic output
scenario_name1= "SCENARIO_1"
scenario_name2= "SCENARIO_2"
scenario_name3= "SCENARIO_3"
scenario_name_4 = "SCENARIO_4"
scenario_name_5=  "SCENARIO_5"

#prompt= SCENARIO_3
# choose the scenario between 1 and 6
UNIFIED_PROMPT1= build_unified_prompt(scenario_name1)
UNIFIED_PROMPT2= build_unified_prompt(scenario_name2)
UNIFIED_PROMPT3= build_unified_prompt(scenario_name3)
UNIFIED_PROMPT4 = build_unified_prompt(scenario_name_4)
UNIFIED_PROMPT5 = build_unified_prompt(scenario_name_5)
CONTACT_PROMPT1 = build_contact_prompt(baseline_coordinator_scenario_1)
CONTACT_PROMPT2 = build_contact_prompt(baseline_coordinator_scenario_2)
CONTACT_PROMPT3 = build_contact_prompt(baseline_coordinator_scenario_3)
CONTACT_PROMPT4 = build_contact_prompt(baseline_coordinator_scenario_4)
CONTACT_PROMPT5 = build_contact_prompt(baseline_coordinator_scenario_5)
MODELS = [
     "mistral",
     "gemma3",
   #"qwen3:32b",
  #"gpt-oss:20b",
  # "gemma3:27b",
  #  "phi4:14b",
  # "deepseek-r1:32b",
    #  "ministral-3:8b",
   "llama3.1:8b",
    # "qwen3"
   # "magistral"
    #"mixtral:8x7b",
 ]

SCENARIOS = [
    ("SCENARIO_1", CONTACT_PROMPT1),
    ("SCENARIO_2", CONTACT_PROMPT2),
    ("SCENARIO_3", CONTACT_PROMPT3),
    ("SCENARIO_4", CONTACT_PROMPT4),
    ("SCENARIO_5", CONTACT_PROMPT5),
 # ("SCENARIO_1", UNIFIED_PROMPT1),
 # ("SCENARIO_2", UNIFIED_PROMPT2),
#  ("SCENARIO_3", UNIFIED_PROMPT3),
 #("SCENARIO_1", SCENARIO_1),
 #("SCENARIO_2", SCENARIO_2),
 #("SCENARIO_3", SCENARIO_3),
# ("SCENARIO_4",  SCENARIO_4 ),
# ("SCENARIO_5",  SCENARIO_5 ),

]

#plan_type = "action+contact_plan"
plan_type= "contact_plan"
provider_type= "local"
provider = "ollama"


# -------------------------------------------------------------------
# Core inference function
# -------------------------------------------------------------------
def run_once(
    model: str,
    prompt: str,
    scenario_name: str,
    keep_alive: str | None = None
) -> Tuple[float, str | None]:
    start_time = time.time()

    try:
        # ------------------------------------------------------------
        # Run inference FIRST
        # ------------------------------------------------------------
        response = chat(
          model=model,
          messages=[{"role": "user", "content": prompt}],
          keep_alive=keep_alive,
          options=OPTIONS,
       )
        output_text = response["message"]["content"]

        # ------------------------------------------------------------
        # Load existing counts
        # ------------------------------------------------------------
        counts_path = _counts_file_path(
            plan_type=plan_type,
            scenario_name=scenario_name,
            provider_type=provider_type,
            provider=provider,
            model=model,
        )

        counts = _load_output_counts(counts_path)
        norm_new = _normalize_text(output_text)

        # ------------------------------------------------------------
        # Update frequency
        # ------------------------------------------------------------
        counts[norm_new] = counts.get(norm_new, 0) + 1

        # ------------------------------------------------------------
        # Save content ONLY if first occurrence
        # ------------------------------------------------------------
        if counts[norm_new] == 1 and output_text.strip():
            print(
                f"[SAVE] New unique output found "
                f"(Model={model}, Scenario={scenario_name})"
            )
            save_content(
                plan_type=plan_type,
                provider_type=provider_type,
                provider=provider,
                prompt=prompt,
                content=output_text,
                scenario_name=scenario_name,
                model=model,
            )
        else:
            print(
                f"[COUNT] Output already seen "
                f"(Model={model}, Scenario={scenario_name}) "
                f"→ count={counts[norm_new]}"
            )

        # ------------------------------------------------------------
        # Persist updated counts
        # ------------------------------------------------------------
        _save_output_counts(counts_path, counts)

    except Exception as e:
        print(f"[WARN] Output comparison/counting failed: {e}")
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
        scenario_name=scenario_name,
        keep_alive=KEEP_ALIVE_WARM,
)

        if total_time != total_time:  # NaN check
            print(f"[ERROR] Model={model} | Trial {trial_idx} returned NaN latency")
        else:
            print(f"[DONE] Model={model} | Trial {trial_idx} | Latency={total_time:.3f}s")

        latencies.append(total_time)
        print(f"Output:\n{output_text}\n")
        # Compare against existing saved outputs for this model in the scenario and save only if unique
                # ------------------------------------------------------------
        # Save output ONLY if it is new for this model + scenario
        # ------------------------------------------------------------
        try:
            existing_outputs = _existing_outputs_for_model(
                plan_type=plan_type,
                scenario_name=scenario_name,
                provider_type=provider_type,
                provider=provider,
                model=model,
            )

            norm_new = _normalize_text(output_text)
            is_unique = True

            for prev in existing_outputs:
                if _normalize_text(prev) == norm_new:
                    is_unique = False
                    break

            if is_unique and isinstance(output_text, str) and output_text.strip():
                print(
                    f"[SAVE] New unique output found "
                    f"(Model={model}, Scenario={scenario_name})"
                )
                print(output_text)
                save_content(
                    plan_type=plan_type,
                    provider_type=provider_type,
                    provider=provider,
                    prompt=prompt,
                    content=output_text,
                    scenario_name=scenario_name,
                    model=model,
                )
            else:
                print(
                    f"[SKIP] Output already seen "
                    f"(Model={model}, Scenario={scenario_name})"
                )

        except Exception as e:
            print(f"[WARN] Output comparison failed: {e}")
    print(f"[END] Scenario={scenario_name} | Model={model}")
    time.sleep(10)  # cooldown between models

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
    time.sleep(10)
    main()
import asyncio
import time
from Prompts import *
from bench_io import save_results, save_content
from agents.llm_assistant_agent import LLMAssistantAgent
from model_clients.ollama_local_client import OllamaLocalModelClient

from ollama_local_model import (
    _counts_file_path,
    _save_output_counts,
    _load_output_counts,
    _normalize_text,
)

# -----------------------------
# Config
# -----------------------------
N_TRIALS = 1
MAX_LOOPS = 8

plan_type = "action+contact_plan"
provider_type = "autogen"
provider = "ollama_local"

# Models
LOCAL_MODELS = [
    "qwen3:32b",
    "gpt-oss:20b",
   # "gemma3:27b",
   # "deepseek-r1:32b",
   # "phi4:14b",
]

ACTION_MODELS = [
  #  "qwen3:32b",
    "deepseek-r1:32b",
]

CRITIC_MODEL = "qwen3:32b"   # 🔒 FIXED

SCENARIOS = [
   # ("SCENARIO_1", SCENARIO_1),
   # ("SCENARIO_2", SCENARIO_2),
    ("SCENARIO_3", SCENARIO_3),
]

# -----------------------------
# Critic helpers (UNCHANGED)
# -----------------------------
def _bundle_for_critic(
    loop_idx: int,
    scenario_prompt: str,
    action_system_prompt: str,
    coordinator_system_prompt: str,
    contact_system_prompt: str,
    plan: str,
    coord_json: str,
    contact_graphs: str,
) -> str:
    return f"""
LOOP #{loop_idx}

==============================
AGENT INPUT SPECIFICATION
==============================

--- SCENARIO (ActionAgent) ---
{scenario_prompt}

--- ActionAgent SYSTEM MESSAGE ---
{action_system_prompt}

--- CoordinatorAgent SYSTEM MESSAGE ---
{coordinator_system_prompt}

--- ContactAgent SYSTEM MESSAGE ---
{contact_system_prompt}

==============================
AGENT OUTPUTS
==============================

--- ACTION PLAN (ActionAgent OUTPUT) ---
{plan}

--- COORDINATOR OUTPUT ---
{coord_json}

--- CONTACT OUTPUT ---
{contact_graphs}

==============================
CRITIC TASK
==============================

You must evaluate the pipeline END-TO-END.

Check the following:

1. Action plan logical correctness:
   - Uses ONLY allowed actions from the scenario
   - Order is logically feasible
   - No missing preconditions or impossible transitions

2. Coordinator correctness:
   - One coordinator entry per action step
   - Objects and interactions correctly reflect the action plan
   - No hallucinated objects or steps

3. Contact graph correctness:
   - One contact graph per coordinator entry
   - Contacts are physically plausible
   - All relevant contacts are included
   - Ends with EXACTLY: ALL INTERACTIONS PROCESSED

4. Global consistency:
   - Action → Coordinator → Contact alignment
   - No missing or extra steps

DECISION RULE:
- If ALL checks pass, reply EXACTLY: APPROVE
- Otherwise, reply starting with: REVISE:
  and list concrete, actionable fixes the ActionAgent must perform.
"""


def _critic_system_message():
    return (
        "You are the CriticAgent. "
        "Approve ONLY if everything is correct."
    )
def _revise_instruction(feedback: str):
    return (
        "The critic identified issues.\n"
        "Revise ONLY the ACTION PLAN to fix them.\n"
        "Do NOT explain.\n"
        "Return ONLY the corrected numbered list.\n\n"
        f"CRITIC FEEDBACK:\n{feedback}"
    )

# -----------------------------
# Agent builders
# -----------------------------
def build_action_agent(model, sys_message):
    return LLMAssistantAgent(
        name="ActionAgent",
        model_client=OllamaLocalModelClient(model=model),
        system_message = sys_message
     )


def build_coordinator_agent(model, sys_message):
    return LLMAssistantAgent(
        name="CoordinatorAgent",
        model_client=OllamaLocalModelClient(model=model),
        system_message = sys_message
    )


def build_contact_agent(model, sys_message):
    return LLMAssistantAgent(
        name="ContactAgent",
        model_client=OllamaLocalModelClient(model=model),
        system_message = sys_message    
    )


def build_critic_agent():
    return LLMAssistantAgent(
        name="CriticAgent",
        model_client=OllamaLocalModelClient(model=CRITIC_MODEL),
        system_message=_critic_system_message(),
    )

# -----------------------------
# One critic loop
# -----------------------------
async def run_until_approved(action_model, coord_model, contact_model, scenario_prompt):
    action_sys = scenario_prompt + "\n\nYou are the ActionAgent. Generate a logically feasible plan using the available actions."
    coord_sys = "You are the CoordinatorAgent. You receive a numbered list of robot actions from the ActionAgent." + coordinator_prompt
    contact_sys = """
You are a helpful assistant in analyzing human-object interactions.

Each message describes one or more specific human-object interactions that occur during a robot manipulation sequence.

You will receive multiple JSON inputs from the CoordinatorAgent.
Return one contact graph per input and end with ALL INTERACTIONS PROCESSED.
---
""" + contact_prompt
    action_agent = build_action_agent(action_model, action_sys)
    coordinator_agent = build_coordinator_agent(coord_model, coord_sys )
    contact_agent = build_contact_agent(contact_model, contact_sys)
    critic_agent = build_critic_agent()

    revision_hint = None
    loops = []

    start = time.time()

    for i in range(1, MAX_LOOPS + 1):
        action_task = (
            "Produce ONLY the numbered action plan.\n\n" + revision_hint
            if revision_hint else
            "Produce ONLY the numbered action plan."
        )

        action_res = await action_agent.run(task=action_task)
        plan = next(m.content for m in reversed(action_res.messages) if m.source == "ActionAgent")

        coord_res = await coordinator_agent.run(task=plan)
        coord_json = next(m.content for m in reversed(coord_res.messages) if m.source == "CoordinatorAgent")

        contact_res = await contact_agent.run(task=coord_json)
        contact_graphs = next(m.content for m in reversed(contact_res.messages) if m.source == "ContactAgent")

        critic_pkg = _bundle_for_critic(
    loop_idx=i,
    scenario_prompt=scenario_prompt,
    action_system_prompt=action_sys,
    coordinator_system_prompt=coord_sys,
    contact_system_prompt=contact_sys,
    plan=plan,
    coord_json=coord_json,
    contact_graphs=contact_graphs,
)
        critic_res = await critic_agent.run(task=critic_pkg)
        verdict = next(m.content for m in reversed(critic_res.messages) if m.source == "CriticAgent")

        loops.append((plan, coord_json, contact_graphs, verdict))

        if verdict.strip().upper().startswith("APPROVE"):
            break

        revision_hint = _revise_instruction(verdict)

    total_latency = time.time() - start

    final_text = "\n\n".join(
        f"[LOOP {i+1}]\nPLAN:\n{p}\n\nCOORD:\n{c}\n\nCONTACT:\n{k}\n\nCRITIC:\n{v}"
        for i, (p, c, k, v) in enumerate(loops)
    )

    return final_text, total_latency

# -----------------------------
# Main runner (FULL SWEEP)
# -----------------------------
async def main():

    for scenario_name, scenario_prompt in SCENARIOS:
        print(f"\n=== SCENARIO {scenario_name} ===")

        for action_model in ACTION_MODELS:
            for coord_model in LOCAL_MODELS:
                for contact_model in LOCAL_MODELS:

                    model_tag = (
                        f"A={action_model}"
                        f"|C={coord_model}"
                        f"|CT={contact_model}"
                        f"|CR={CRITIC_MODEL}"
                    )

                    print(f"\n--- {model_tag} ---")

                    for t in range(N_TRIALS):

                        output, latency = await run_until_approved(
                            action_model,
                            coord_model,
                            contact_model,
                            scenario_prompt,
                        )

                        counts_path = _counts_file_path(
                            plan_type,
                            scenario_name,
                            provider_type,
                            provider,
                            model_tag,
                        )

                        counts = _load_output_counts(counts_path)
                        norm = _normalize_text(output)
                        counts[norm] = counts.get(norm, 0) + 1

                        if counts[norm] == 1:
                            print("[SAVE] New output")
                            save_content(
                                plan_type= plan_type,
                                provider_type= provider_type,
                                provider= provider,
                                model = model_tag,
                                prompt = scenario_prompt,
                                content = output,
                                scenario_name= scenario_name,
                            )
                        else:
                            print("[SKIP] Duplicate output")

                        _save_output_counts(counts_path, counts)

                        save_results(
                            plan_type,
                            provider_type,
                            provider,
                            model_tag,
                            [latency],
                            scenario_name,
                        )

                        print(f"Trial {t+1}/{N_TRIALS} | {latency:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
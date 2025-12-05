import asyncio
import time
from typing import List
from Prompts import SCENARIO_1, coordinator_prompt, contact_prompt
from bench_io import save_results, save_content
from agents.llm_assistant_agent import LLMAssistantAgent
from model_clients import GeminiModelClient, OllamaModelClient
from dotenv import load_dotenv, find_dotenv
import os

plan_type = "action+contact_plan"
provider_type = "autogen"
provider = "multiple_providers"
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
# -----------------------------
# Config
# -----------------------------
scenario_name = "SCENARIO_1"
scenario_text = SCENARIO_1

N_WARM_TRIALS = 1
MAX_LOOPS = 8
SLEEP_BETWEEN_LOOPS_SEC = 0.0  # set >0 if you want a small delay
# Model clients
action_model = "gemini-2.5-pro"
action_client = GeminiModelClient(
    model=action_model,
    api_key = GEMINI_API_KEY,
)
coordinator_model = "gemini-2.5-flash-lite"
coordinator_client = GeminiModelClient(
    model=coordinator_model,
    api_key=GEMINI_API_KEY,
)
contact_model = "qwen3-vl:235b-cloud"
contact_client = OllamaModelClient(
    model=contact_model,
    api_key=OLLAMA_API_KEY,
)
critic_model = "qwen3-vl:235b-cloud"
critic_client = OllamaModelClient(
    model=contact_model,
    api_key=OLLAMA_API_KEY,
)


# -----------------------------
# Helpers
# -----------------------------
def _bundle_for_critic(loop_idx: int, plan: str, coord_json: str, contact_graphs: str) -> str:
    """
    Compose one review package for the critic (whole pipeline output of the loop).
    """
    return (
        f"LOOP #{loop_idx}\n\n"
        "=== ACTION PLAN ===\n"
        f"{plan}\n\n"
        "=== COORDINATOR_OUTPUT (JSON array) ===\n"
        f"{coord_json}\n\n"
        "=== CONTACT_OUTPUT (graphs) ===\n"
        f"{contact_graphs}\n\n"
        "=== CRITIC TASK ===\n"
        "Evaluate logical/physical feasibility and spec compliance:\n"
        " - ACTION_PLAN must be a numbered list per scenario rules (no extra text).\n"
        " - COORDINATOR_OUTPUT must be a pure JSON array of objects with keys exactly "
        '   {"objects", "interaction"} in the same order as the action lines.\n'
        " - CONTACT_OUTPUT must return a list of JSON graphs (same order), then write exactly:\n"
        "   ALL INTERACTIONS PROCESSED\n\n"
        "If everything is correct, reply EXACTLY: APPROVE\n"
        "Otherwise, reply with a short, actionable critique starting with: REVISE:\n"
        "and list concrete fixes the ActionAgent must perform.\n"
    )


def _critic_system_message() -> str:
    return (
        "You are the Critic. You review the entire pipeline output (Action plan, "
        "Coordinator mapping, Contact graphs). Approve only if:\n"
        "1) The action plan satisfies the scenario rules.\n"
        "2) The coordinator JSON is the correct shape (objects + interaction) and order.\n"
        "3) The contact graphs are plausible and end with ALL INTERACTIONS PROCESSED.\n"
        "Respond EXACTLY 'APPROVE' when satisfied. Otherwise, start with 'REVISE:' and "
        "list concrete issues to fix.\n"
    )


def _revise_instruction(critic_feedback: str) -> str:
    """
    Instruction injected to ActionAgent when revision is needed.
    """
    return (
        "The critic responded with issues. Revise your plan accordingly.\n"
        "Return ONLY the corrected numbered action list (no extra text).\n\n"
        f"CRITIC FEEDBACK:\n{critic_feedback}\n"
    )


# -----------------------------
# Build agents (you attach your model clients)
# -----------------------------
def build_action_agent() -> LLMAssistantAgent:
    return LLMAssistantAgent(
        name="ActionAgent",
        model_client=action_client,
        # The scenario is the system message. The task text will ask for numbered list only.
        system_message=scenario_text,
    )


def build_coordinator_agent() -> LLMAssistantAgent:
    return LLMAssistantAgent(
        name="CoordinatorAgent",
        model_client=coordinator_client,
        system_message=coordinator_prompt,
    )


def build_contact_agent() -> LLMAssistantAgent:
    return LLMAssistantAgent(
        name="ContactAgent",
        model_client=contact_client,
        system_message=contact_prompt,
    )


def build_critic_agent() -> LLMAssistantAgent:
    return LLMAssistantAgent(
        name="CriticAgent",
        model_client=critic_client,
        system_message=_critic_system_message(),
    )


# -----------------------------
# One full pipeline loop
# -----------------------------
async def run_one_loop(loop_idx: int, action_agent: LLMAssistantAgent,
                       coordinator_agent: LLMAssistantAgent,
                       contact_agent: LLMAssistantAgent,
                       critic_agent: LLMAssistantAgent,
                       revision_hint: str | None) -> dict:
    """
    Runs Action -> Coordinator -> Contact -> Critic once.
    If revision_hint is provided, it's appended as the task for ActionAgent to revise.
    Returns a dict with all stage outputs plus critic verdict.
    """
    # --- ACTION ---
    if revision_hint:
        action_task = (
            "Produce ONLY the numbered action plan per the scenario. No extra text.\n\n"
            + revision_hint
        )
    else:
        action_task = "Produce ONLY the numbered action plan per the scenario. No extra text."

    action_res = await action_agent.run(task=action_task)
    # Last content from ActionAgent (LLMAssistantAgent typically sets .source to agent name)
    plan = ""
    for m in reversed(action_res.messages):
        if m.source == "ActionAgent":
            plan = m.content.strip()
            break

    # --- COORDINATOR ---
    coord_res = await coordinator_agent.run(task=plan)
    coord_json = ""
    for m in reversed(coord_res.messages):
        if m.source == "CoordinatorAgent":
            coord_json = m.content.strip()
            break

    # --- CONTACT ---
    contact_res = await contact_agent.run(task=coord_json)
    contact_graphs = ""
    for m in reversed(contact_res.messages):
        if m.source == "ContactAgent":
            contact_graphs = m.content.strip()
            break

    # --- CRITIC ---
    critic_pkg = _bundle_for_critic(loop_idx, plan, coord_json, contact_graphs)
    critic_res = await critic_agent.run(task=critic_pkg)
    critic_out = ""
    for m in reversed(critic_res.messages):
        if m.source == "CriticAgent":
            critic_out = m.content.strip()
            break

    return {
        "plan": plan,
        "coord_json": coord_json,
        "contact_graphs": contact_graphs,
        "critic_output": critic_out,
        "transcripts": {
            "action": action_res.messages,
            "coordinator": coord_res.messages,
            "contact": contact_res.messages,
            "critic": critic_res.messages,
        }
    }


# -----------------------------
# Runner (with approval loop)
# -----------------------------
async def run_until_approved(max_loops: int = MAX_LOOPS) -> tuple[float, dict]:
    start = time.time()

    action_agent = build_action_agent()
    coordinator_agent = build_coordinator_agent()
    contact_agent = build_contact_agent()
    critic_agent = build_critic_agent()

    revision_hint = None
    all_loops: List[dict] = []

    for i in range(1, max_loops + 1):
        result = await run_one_loop(
            loop_idx=i,
            action_agent=action_agent,
            coordinator_agent=coordinator_agent,
            contact_agent=contact_agent,
            critic_agent=critic_agent,
            revision_hint=revision_hint,
        )
        all_loops.append(result)

        if result["critic_output"].strip().upper().startswith("APPROVE"):
            end = time.time()
            return end - start, {"loops": all_loops, "approved": True, "final": result}

        # Not approved → pass critique to ActionAgent next round
        revision_hint = _revise_instruction(result["critic_output"])
        if SLEEP_BETWEEN_LOOPS_SEC:
            await asyncio.sleep(SLEEP_BETWEEN_LOOPS_SEC)

    end = time.time()
    return end - start, {"loops": all_loops, "approved": False, "final": all_loops[-1]}


# -----------------------------
# Save helpers
# -----------------------------
def _render_full_transcript(payload: dict) -> str:
    """
    Pretty-print all loops for save_content().
    """
    out_lines = []
    for idx, item in enumerate(payload["loops"], 1):
        out_lines.append(f"\n--- LOOP {idx} ---")
        out_lines.append("\n[PLAN]\n" + item["plan"])
        out_lines.append("\n[COORDINATOR_OUTPUT]\n" + item["coord_json"])
        out_lines.append("\n[CONTACT_OUTPUT]\n" + item["contact_graphs"])
        out_lines.append("\n[CRITIC]\n" + item["critic_output"])
    out_lines.append(f"\n\n=== APPROVED: {payload['approved']} ===\n")
    return "\n".join(out_lines)


# -----------------------------
# Main
# -----------------------------
async def main():
    # Sanity: ensure clients are provided
    if not all([action_client, coordinator_client, contact_client, critic_client]):
        raise RuntimeError("Please set action_client, coordinator_client, contact_client, critic_client.")

    print("Running Action→Coordinator→Contact→Critic loop until APPROVE...")
    total_latency, payload = await run_until_approved(MAX_LOOPS)

    # Model tag (adjust to your actual model names if you like)
    model_tag = "pipeline_action+coordinator+contact_then_critic"

    # Save transcript
    transcript = _render_full_transcript(payload)
    save_content(
        plan_type= "action+contact_plan",
        provider_type="autogen",
        provider="multiple_providers",
        prompt=scenario_text,
        content=transcript,
        scenario_name=scenario_name,
        model= action_model+contact_model+coordinator_model,
    )

    # Save latency
    save_results(
        provider_type=provider_type,
        provider=provider,
        plan_type=plan_type,
        total_latency=[total_latency],
        scenario_name=scenario_name,
        model= action_model+contact_model+coordinator_model,
    )

    print(f"\nApproved: {payload['approved']}. Total latency: {total_latency:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
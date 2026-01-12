import asyncio
import time
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from Prompts import *
from bench_io import save_content
from agents.llm_assistant_agent import LLMAssistantAgent
from model_clients.ollama_local_client import OllamaLocalModelClient

def print_messages(messages, title=None):
    if title:
        print("\n" + "=" * 80)
        print(title)
        print("=" * 80)

    for i, m in enumerate(messages, 1):
        print(f"\n[{i}] {m.source}")
        print("-" * (len(m.source) + 4))
        print(m.content.strip())
CRITIC_PROMPT = """
You are a validation agent.

You receive:
1) A scene description (scenario), which defines the environment, objects, constraints, and available actions.
2) A numbered list of robot actions generated for that scenario.

Your task:
- Verify whether the action plan satisfies ALL constraints imposed by the scenario.
- Constraints include (but are not limited to):
  - Object locations and distances
  - Action preconditions and ordering
  - Action definitions and allowed actions
  - Capacity limits (e.g., trolley capacity)
  - Mandatory actions triggered by distance or height constraints
  - Physical feasibility of locomotion and object transport

Output rules:
- If the plan fully satisfies all constraints and is valid, output exactly:
  APPROVE
- If the plan is invalid, output ONLY a numbered list of missing, incorrect, or invalid actions.

Strict rules:
- Do NOT explain.
- Do NOT justify.
- Do NOT mention yourself or any agent roles.
- Do NOT say "revised plan".
- Do NOT repeat the full action plan.
- Do NOT add any text outside the required output.
- Output must be machine-readable.
"""     
        
# -----------------------------
# Config
# -----------------------------
ACTION_MODEL = "qwen3:32b"
CRITIC_MODEL = "deepseek-r1:32b"
OUTER_MODEL = "gpt-oss:20b"

N_TRIALS = 1

provider_type = "autogen"
provider = "ollama_local"
plan_type = "reflection_then_grounding"

# -----------------------------
# Build Reflection Team
# -----------------------------
def build_reflection_team():

    action_agent = LLMAssistantAgent(
        name="ActionAgent",
        model_client=OllamaLocalModelClient(model=ACTION_MODEL),
        system_message= SCENARIO_3,
        temperature=0.0,
    )

    critic_agent = LLMAssistantAgent(
    name="CriticAgent",
    model_client=OllamaLocalModelClient(model=CRITIC_MODEL),
    description="Validates action plans against scenario constraints.",
    system_message=(
        "This is the scenario description:\n\n"
        + SCENARIO_3
        + "\n\n"
        + CRITIC_PROMPT  # the text above
    ),
    temperature=0.0,
)
    termination = TextMentionTermination("APPROVE")

    return RoundRobinGroupChat(
        participants=[action_agent, critic_agent],
        termination_condition=termination,
        max_turns=30,
    )

# -----------------------------
# Build Outer Team (Coordinator → Contact)
# -----------------------------
def build_outer_team():

    shared_client = OllamaLocalModelClient(model=OUTER_MODEL)

    coordinator_agent = LLMAssistantAgent(
        name="CoordinatorAgent",
        model_client=shared_client,
        system_message=(
            "You are the CoordinatorAgent. "
            "You receive a numbered list of robot actions from the ActionAgent."
            + coordinator_prompt
        ),
    )

    contact_agent = LLMAssistantAgent(
        name="ContactAgent",
        model_client=shared_client,
        system_message=(
            """
You are a helpful assistant in analyzing human-object interactions.

Each message describes one or more specific human-object interactions that occur during a robot manipulation sequence.

You will receive multiple JSON inputs from the CoordinatorAgent.
Your task is to process each input individually, generate a separate JSON graph for each,
and return a list of all JSON graphs in the same order as the inputs.

After you finish processing all inputs, you must write exactly: ALL INTERACTIONS PROCESSED
---
"""
            + contact_prompt
        ),
    )

    termination = TextMentionTermination("ALL INTERACTIONS PROCESSED")

    return RoundRobinGroupChat(
        participants=[coordinator_agent, contact_agent],
        termination_condition=termination,
        max_turns=2,
    )

# -----------------------------
# Utility: extract final approved plan
# -----------------------------
def extract_final_action_plan(messages):
    for msg in reversed(messages):
        if msg.source == "ActionAgent":
            return msg.content.strip()
    raise RuntimeError("No ActionAgent output found.")

# -----------------------------
# Main
# -----------------------------
async def main():
    for trial in range(1, N_TRIALS + 1):

        print("\n==============================")
        print(f"Trial {trial}: Reflection loop")
        print("==============================")

        # -------- Stage 1: Reflection --------
        reflection_team = build_reflection_team()
        start_reflection = time.time()
        reflection_result = await reflection_team.run()
        print_messages(
    reflection_result.messages,
    title="REFLECTION LOOP — FULL TRANSCRIPT"
)
        reflection_latency = round(time.time() - start_reflection, 3)

        final_plan = extract_final_action_plan(reflection_result.messages)

        print("\nFinal APPROVED Action Plan:\n")
        print(final_plan)

        # -------- Stage 2: Grounding --------
        print("\n==============================")
        print("Grounding loop (Coordinator → Contact)")
        print("==============================")

        outer_team = build_outer_team()
        start_outer = time.time()
        outer_result = await outer_team.run(task=final_plan)
        outer_latency = round(time.time() - start_outer, 3)

        # -------- Save combined output --------
        combined_output = (
            "=== FINAL APPROVED ACTION PLAN ===\n"
            + final_plan
            + "\n\n=== REFLECTION TRANSCRIPT ===\n"
            + "\n".join(f"{m.source}: {m.content}" for m in reflection_result.messages)
            + "\n\n=== COORDINATOR + CONTACT OUTPUT ===\n"
            + "\n".join(f"{m.source}: {m.content}" for m in outer_result.messages)
        )
        print(combined_output)
        #save_content(
        #    plan_type=plan_type,
        #    provider_type=provider_type,
        #    provider=provider,
        #    model=f"{ACTION_MODEL}+{CRITIC_MODEL}+{OUTER_MODEL}",
        #    prompt="",
        #    content=combined_output,
        #    scenario_name="SCENARIO_3",
        #)

        print(f"\nReflection latency: {reflection_latency}s")
        print(f"Grounding latency:  {outer_latency}s")
        print("=== DONE ===\n")

        await asyncio.sleep(5)

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
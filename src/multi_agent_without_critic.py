import asyncio
import time
import math
from bench_io import save_results, save_content
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from Prompts import *
from agents.llm_assistant_agent import LLMAssistantAgent
from model_clients import GeminiModelClient
from model_clients.ollama_client import OllamaModelClient
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
# -----------------------------
# Config
# -----------------------------
N_TRIALS = 1
action_model = "gemini-robotics-er-1.5-preview"
action_client = GeminiModelClient(
    model=action_model,
    api_key = GEMINI_API_KEY,
)
coordinator_model = "gemini-robotics-er-1.5-preview"
coordinator_client = GeminiModelClient(
    model=coordinator_model,
    api_key=GEMINI_API_KEY,
)
#contact_model = "gemini-2.5-pro"
contact_model = "glm-4.6:cloud"
contact_client = OllamaModelClient(
    model=contact_model,
    api_key=OLLAMA_API_KEY,
)
plan_type = "action+contact_plan"
provider_type = "autogen"
provider = "multiple_providers"

prompt = SCENARIO_1
scenario_name = "SCENARIO_1"
# -----------------------------
# Multi-agent setup
# -----------------------------
def build_inner_team():
    contact_agent = LLMAssistantAgent(
        name="ContactAgent",
        description="Analyzes human-object contact relations and returns JSON graph of interactions.",
        model_client=contact_client,
        system_message="""
You are a helpful assistant in analyzing human-object interactions.

Each message describes one or more specific human-object interactions that occur during a robot manipulation sequence.

You will receive **multiple JSON inputs** from the CoordinatorAgent, each describing a separate interaction step.  
Your task is to **process each input individually**, generate a separate JSON graph for each,  
and return **a list of all JSON graphs** in the same order as the inputs.  

After you finish processing all inputs, you must write exactly: **ALL INTERACTIONS PROCESSED**

---""" + contact_prompt,
    )
    coordinator_agent = LLMAssistantAgent(
        name="CoordinatorAgent",
        description="Converts ActionAgent plan into JSON inputs and sends them to ContactAgent.",
        model_client=coordinator_client,
        system_message="You are the CoordinatorAgent. You receive a numbered list of robot actions from the ActionAgent."
                       + coordinator_prompt,
    )
    termination = TextMentionTermination("ALL INTERACTIONS PROCESSED")
    # Round-robin (Coordinator → Contact)
    team = RoundRobinGroupChat(
        participants=[coordinator_agent, contact_agent],
        max_turns=2,
        termination_condition=termination,
    )
    return team


def build_action_agent():
    return LLMAssistantAgent(
        name="ActionAgent",
        model_client=action_client,
        system_message=prompt + "\n\n"
        "You are the ActionAgent. Generate a logically feasible plan using the available actions.",
    )


# -----------------------------
# Benchmark helpers
# -----------------------------
async def run_once_multi_agent() -> float:
    """Run the ActionAgent once, then the Coordinator and Contact stage."""
    try:
        start = time.time()

        # ActionAgent generating the plan
        action_agent = build_action_agent()
        print("\n[ActionAgent] Generating plan...")
        action_result = await action_agent.run()
        final_plan = ""
        for msg in reversed(action_result.messages):
            if msg.source == "ActionAgent":
                final_plan = msg.content.strip()
                break

        print("\n[ActionAgent] Final plan:\n", final_plan)

        # Run Coordinator + Contact
        main_team = build_inner_team()
        print("\n[Coordinator + Contact] Processing plan...")
        inner_result = await main_team.run(task=final_plan)

        # Save results
        end = time.time()
        total = end - start
        model_tag = f"multi_agent_no_critic_{contact_model}_{action_model}"

        save_content(
            plan_type=plan_type,
            provider_type=provider_type,
            provider=provider,
            model=model_tag,
            prompt=prompt,
            content="\n\n--- ACTION STAGE ---\n\n"
                    + final_plan
                    + "\n\n--- COORDINATION STAGE ---\n\n"
                    + "\n\n".join(f"{m.source}: {m.content}" for m in inner_result.messages),
            scenario_name=scenario_name
        )
        save_results(
            plan_type=plan_type,
            provider_type=provider_type,
            provider=provider,
            model=model_tag,
            total_latency=[total],
            scenario_name=scenario_name
        )
        return total
    except Exception as e:
        print(f"[multi-agent] error: {e}")
        return math.nan

    

# -----------------------------
# Main Runner
# -----------------------------
async def main():
    MODEL_NAME = f"Multi-Agent No-Critic ({contact_model}+{action_model})"
    print(f"Benchmarking {MODEL_NAME} setup...")
    results = []
    for i in range (N_TRIALS):
        total = await run_once_multi_agent ()
        print (f"[multi-agent] WARM {i + 1}/{N_TRIALS}: Total={total:.3f}s")
        results.append (total)
        await asyncio.sleep (10)  # short delay between trials
    return results


if __name__ == "__main__":
    asyncio.run(main())

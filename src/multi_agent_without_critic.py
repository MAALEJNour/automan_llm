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
from model_clients.ollama_local_client import OllamaLocalModelClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

LOCAL_MODELS = [
    "qwen3:32b",
    "gpt-oss:20b",
    "gemma3:27b",
    "deepseek-r1:32b",
    "phi4:14b",
]
SCENARIOS = [
    ("SCENARIO_1", SCENARIO_1),
    ("SCENARIO_2", SCENARIO_2),
    ("SCENARIO_3", SCENARIO_3),
 #  ("SCENARIO_MAKING_COFFEE", SCENARIO_MAKING_COFFEE), 
 #  ("SCENARIO_CLEANING_HOME", SCENARIO_CLEANING_HOME),
 # both these scenarios are very long and take much time 
]
 

# -----------------------------
# Config
# -----------------------------
N_TRIALS = 1
#action_client = OllamaLocalModelClient(
#    model=action_model,
   # api_key = GEMINI_API_KEY,
#)
#coordinator_model = "gemini-robotics-er-1.5-preview"
#coordinator_model = "deepseek-r1:32b"
#coordinator_client = OllamaLocalModelClient(
  #  model=coordinator_model,
   # api_key=GEMINI_API_KEY,
#)
#contact_model = "deepseek-r1:32b"

#contact_model = "gemini-2.5-pro"
#contact_model = "glm-4.6:cloud"
#contact_client = OllamaModelClient(
#    model=contact_model,
#    api_key=OLLAMA_API_KEY,
#)
plan_type = "action+contact_plan"
provider_type = "autogen"
provider = "ollama_local"
#prompt = SCENARIO_1
#scenario_name = "SCENARIO_1"
#
#action_client = OllamaModelClient(
#    model="",
#    keep_alive="30m",
#    options={
#        "num_ctx": 8192,
#        "top_p": 0.9,
#    },
#)
#
# -----------------------------
# Multi-agent setup
# -----------------------------
def build_inner_team(shared_model: str):
    shared_client = OllamaLocalModelClient(model=shared_model)
    contact_agent = LLMAssistantAgent(
        name="ContactAgent",
        description="Analyzes human-object contact relations and returns JSON graph of interactions.",
        model_client=shared_client,
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
        model_client=shared_client,
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



def build_action_agent(action_model: str, scenario_prompt: str):
    action_client = OllamaLocalModelClient(model=action_model)

    return LLMAssistantAgent(
        name="ActionAgent",
        model_client=action_client,
        system_message=scenario_prompt + "\n\n"
        "You are the ActionAgent. Generate a logically feasible plan using the available actions.",
    )


# -----------------------------
# Benchmark helpers
# -----------------------------
async def run_once_multi_agent(
    action_model: str,
    shared_model: str,
    scenario_name: str,
    scenario_prompt: str,
) -> float:
    try:
        start = time.time()

        # Action stage
        action_agent = build_action_agent(action_model, scenario_prompt)
        print(f"\n[ActionAgent:{action_model}] ({scenario_name}) Generating plan...")
        action_result = await action_agent.run()

        final_plan = ""
        for msg in reversed(action_result.messages):
            if msg.source == "ActionAgent":
                final_plan = msg.content.strip()
                break

        # Coordinator + Contact stage
        team = build_inner_team(shared_model)
        print(f"[Coordinator+Contact:{shared_model}] ({scenario_name}) Processing plan...")
        inner_result = await team.run(task=final_plan)

        total = time.time() - start

        model_tag = f"A={action_model}__CC={shared_model}"

        save_content(
            plan_type=plan_type,
            provider_type=provider_type,
            provider=provider,
            model=model_tag,
            prompt=scenario_prompt,
            content=(
                "\n--- ACTION ---\n" + final_plan +
                "\n\n--- COORD+CONTACT ---\n" +
                "\n".join(f"{m.source}: {m.content}" for m in inner_result.messages)
            ),
            scenario_name=scenario_name,
        )

        save_results(
            plan_type=plan_type,
            provider_type=provider_type,
            provider=provider,
            model=model_tag,
            total_latency=[total],
            scenario_name=scenario_name,
        )

        return total

    except Exception as e:
        print(f"[ERROR {scenario_name} A={action_model} CC={shared_model}] {e}")
        return math.nan

# -----------------------------
# Main Runner
# -----------------------------
async def main():
    print("Running all scenarios × action models × coordinator/contact models")

    for scenario_name, scenario_prompt in SCENARIOS:
        print(f"\n==============================")
        print(f"=== SCENARIO: {scenario_name} ===")
        print(f"==============================")

        for action_model in LOCAL_MODELS:
            for shared_model in LOCAL_MODELS:

                combo_name = f"{scenario_name} | A={action_model} | CC={shared_model}"
                print(f"\n--- {combo_name} ---")

                results = []
                for i in range(N_TRIALS):
                    total = await run_once_multi_agent(
                        action_model=action_model,
                        shared_model=shared_model,
                        scenario_name=scenario_name,
                        scenario_prompt=scenario_prompt,
                    )

                    print(
                        f"[{combo_name}] "
                        f"Trial {i+1}/{N_TRIALS}: {total:.3f}s"
                    )
                    results.append(total)

                    #await asyncio.sleep(10)  # cooldown needed only for local models to not exceed usage limit


if __name__ == "__main__":
    asyncio.run(main())

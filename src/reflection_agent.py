import asyncio
import time
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from Prompts import *
from bench_io import save_content
from agents.llm_assistant_agent import LLMAssistantAgent
from model_clients import GeminiModelClient
from model_clients.ollama_client import OllamaModelClient
import os
from dotenv import load_dotenv, find_dotenv
# -----------------------------
# Config
# -----------------------------
action_model ="gemini-2.0-flash-lite"
critic_model = "deepseek-v3.1:671b-cloud" # needs to be ollama
N_TRIALS = 1
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
critic_client = OllamaModelClient(
    model=critic_model,
    api_key=OLLAMA_API_KEY,
)
action_client = GeminiModelClient(
    model=action_model,
    api_key=GEMINI_API_KEY,
)
plan_type= "action_plan_reflection"
provider_type="autogen"
provider= "multiple_providers"
# -----------------------------
# Build Reflection Team
# -----------------------------
def build_reflection_team():

    action_agent = LLMAssistantAgent(
        name="ActionAgent",
        model_client=action_client,
        system_message=(
                SCENARIO_3 + "\n\n"
               "You are collaborating with a CriticAgent who reviews your plans. "
                "After each critique, revise your plan based on the feedback before resubmitting. "
                "Do not repeat the same plan unless it fully addresses the critic's comments. "
                "When your plan seems correct, stop revising further."
        ),
        temperature=0.0,
    )
    critic_agent = LLMAssistantAgent(
        name="CriticAgent",
        model_client=critic_client,
        description="Critiques the ActionAgent's plan. Respond with 'APPROVE' if the plan is logically feasible.",
        system_message=(
                "This is the prompt given to the ActionAgent, which defines its environment and available actions:\n\n"
                + SCENARIO_3
                + "\n\nYou are the CriticAgent. Your task is to evaluate the ActionAgent's plan for logical feasibility "
                  "based on the problem and allowed actions above. Provide clear and constructive feedback when the plan "
                  "has flaws or can be improved. When the plan fully addresses your feedback and is logically feasible, "
                  "respond only with 'APPROVE'."
        ),
        temperature=0.0,
    )
    termination = TextMentionTermination("APPROVE")
    reflection_team = RoundRobinGroupChat(
        participants=[action_agent, critic_agent],
        termination_condition=termination,
        max_turns=30
    )
    return reflection_team

async def main():
    for i in range(1, N_TRIALS + 1):
        team = build_reflection_team()
        print("Running reflection loop...")
        start = time.time()
        result = await team.run()
        total = round(time.time() - start, 4)  # seconds rounded to 4 decimals
        #print(f"\n Trial {i} latency : {total} seconds")
        # Save chat content
        save_content(
            provider_type= provider_type,
            provider = provider,

            model= critic_model+ action_model,
            prompt="",
            content= "\n\n".join(f"{m.source}: {m.content}" for m in result.messages),
            scenario_name="scenario_3",
        )
        # Save latency to JSON file
        #save_results("autogen", f"{critic_model}+{action_model}", [total])
        print("\n=== Reflection finished ===")
        time.sleep(20)

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
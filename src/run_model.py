import time
import math
import asyncio
from typing import List
from ollama import chat
from google import genai
from openai import OpenAI
from huggingface_hub import AsyncInferenceClient
from bench_io import save_content
import os
from dotenv import load_dotenv, find_dotenv


# Deterministic config
TEMPERATURE = 0.0
SLEEP_BETWEEN = 20  # seconds between requests to simulate cooldowns


# API KEYS
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Clients
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
open_router_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)
hf_client = AsyncInferenceClient(
    base_url="https://router.huggingface.co",
    token=HF_TOKEN
)


def _valid_latency(x) -> bool:
    """True if x is a finite number (non-NaN, non-inf)."""
    return isinstance(x, (int, float)) and math.isfinite(x)


def run_once_ollama(model: str, prompt: str, scenario_name: str, plan_type : str, provider_type : str) -> float:
    """Runs one Ollama request (local or cloud) and returns ONLY total latency."""
    start = time.time()
    try:
        response = chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        end = time.time()
        total = end - start

        text = response["message"]["content"]
        save_content (
            plan_type=plan_type,
            provider="ollama",
            provider_type=provider_type,
            prompt=prompt,
            content=text,
            scenario_name=scenario_name,
            model=model,
        )
        return total

    except Exception as e:
        print(f"[{model}] error: {e}")
        return math.nan


def run_once_gemini(model: str, prompt: str, scenario_name: str, plan_type : str,  provider_type : str ) -> float:
    start = time.time()
    try:
        response = gemini_client.models.generate_content(model=model, contents=prompt)
        end = time.time()
        total = end - start
        save_content (
            plan_type=plan_type,
            provider="gemini",
            provider_type=provider_type,
            prompt=prompt,
            content=response.text,
            scenario_name=scenario_name,
            model=model,
        )
        return total
    except Exception as e:
        print(f"[{model}] error: {e}")
        return math.nan


def run_once_openrouter(model: str, prompt: str, scenario_name: str , plan_type : str ,  provider_type : str ) -> float:
    start = time.time()
    try:
        response = open_router_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
        )
        end = time.time()
        total = end - start

        text = response.choices[0].message.content if response.choices else ""
        save_content (
            plan_type=plan_type,
            provider="openrouter",
            provider_type= provider_type,
            prompt=prompt,
            content=response.text,
            scenario_name=scenario_name,
            model=model,
        )
        return total
    except Exception as e:
        print(f"[{model}] error: {e}")
        return math.nan


async def run_once_huggingface(model: str, prompt: str, scenario_name: str, plan_type : str, provider_type : str) -> float:
    start = time.time()
    try:
        response = await hf_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=32768,
            temperature=0.0,
        )
        end = time.time()
        total = end - start

        text = response.choices[0].message["content"]
        save_content (
            plan_type=plan_type,
            provider="huggingface",
            prompt=prompt,
            provider_type= provider_type,
            content=response.text,
            scenario_name=scenario_name,
            model=model,
        )
        return total
    except Exception as e:
        print(f"[{model}] error: {e}")
        return math.nan


def _run_hf_sync(model: str, prompt: str, scenario_name: str, plan_type: str, provider_type : str) -> float:
    """Synchronous wrapper for the async HuggingFace call."""
    return asyncio.run(run_once_huggingface(model, prompt, scenario_name, plan_type , provider_type))


def run_n_trials(model: str, n: int, prompt: str, scenario_name: str, provider: str, plan_type: str, provider_type : str ) -> List[float]:
    """
    Run until we collect exactly n VALID (finite) latencies.
    Failed attempts (NaN/inf/errors) are skipped and retried.
    """
    results: List[float] = []
    attempt = 0

    while len(results) < n:
        attempt += 1

        if provider == "gemini":
            total = run_once_gemini(model, prompt, scenario_name,plan_type,provider_type)
        elif provider == "openrouter":
            total = run_once_openrouter(model, prompt, scenario_name,plan_type,provider_type)
        elif provider == "huggingface":
            total = _run_hf_sync(model, prompt, scenario_name,plan_type, provider_type)
        elif provider == "ollama":
            total = run_once_ollama(model, prompt, scenario_name,plan_type, provider_type)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        if _valid_latency(total):
            print(f"[{model}] WARM {len(results)+1:02d}/{n} (attempt {attempt}): Total={total:.3f}s")
            results.append(total)
        else:
            print(f"[{model}] attempt {attempt}: invalid latency (NaN/inf). Retrying…")

        # rate-limit pause even after failures (safer with provider limits)
        time.sleep(SLEEP_BETWEEN)

    return results
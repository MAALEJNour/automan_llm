# model_clients/openrouter_client.py
from __future__ import annotations
from typing import List, Dict, Tuple
from autogen_core.model_context import UnboundedChatCompletionContext
from openai import OpenAI
from .base import BaseModelClient


class OpenRouterModelClient(BaseModelClient):
    """
    Correct implementation using OpenRouter's OpenAI-compatible Chat API.
    This *exactly* matches your OpenRouterAssistantAgent logic.
    """

    def __init__(self, model: str, api_key: str):
        self._model = model
        self._api_key = api_key
        self._model_context = UnboundedChatCompletionContext()
        # THIS IS CORRECT (OpenRouter docs)
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
    ) -> Tuple[str, int, int]:

        # ---- Call OpenRouter via OpenAI-compatible interface ----
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
        )

        # ---- Extract text ----
        text = completion.choices[0].message.content

        # ---- Extract usage ----
        usage = completion.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens

        return text, prompt_tokens, completion_tokens

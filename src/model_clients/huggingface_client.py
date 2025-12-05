# model_clients/huggingface_client.py
from __future__ import annotations
from typing import List, Dict, Tuple
import os
from huggingface_hub import AsyncInferenceClient
from .base import BaseModelClient


class HuggingFaceModelClient(BaseModelClient):
    """
    Uses HF Inference API (router) with OpenAI-style /chat/completions.
    """

    def __init__(
        self,
        model: str,
        api_token_env: str = "HUGGINGFACEHUB_API_TOKEN",
    ):
        self._model = model
        token = os.getenv(api_token_env, "")
        self._client = AsyncInferenceClient(
            base_url="https://router.huggingface.co",
            token=token,
        )

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
    ) -> Tuple[str, int, int]:
        completion = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=2048,
        )

        text = completion.choices[0].message.content
        usage = completion.usage

        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens

        return text, prompt_tokens, completion_tokens
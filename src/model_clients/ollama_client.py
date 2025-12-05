# model_clients/ollama_client.py
from __future__ import annotations
from typing import List, Dict, Tuple
from ollama import Client
from .base import BaseModelClient
import asyncio


class OllamaModelClient(BaseModelClient):
    """
    Clean model client that replicates the exact behavior of your
    existing OllamaAssistantAgent using the Ollama Python SDK.
    """

    def __init__(self, model: str, api_key: str):
        self._model = model

        # EXACT same behavior as in your original agent:
        self._client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {api_key}"}
        )

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
    ) -> Tuple[str, int, int]:

        # Ollama client is synchronous → run in thread
        def _sync_call():
            return self._client.chat(
                model=self._model,
                messages=messages,
                options={"temperature": temperature},
            )

        completion = await asyncio.get_running_loop().run_in_executor(None, _sync_call)

        # Extract text exactly as before
        text = completion["message"]["content"]

        # Token counting identical to your agent
        prompt_tokens = len(" ".join(m.get("content", "") for m in messages).split())
        completion_tokens = len(text.split())

        return text, prompt_tokens, completion_tokens

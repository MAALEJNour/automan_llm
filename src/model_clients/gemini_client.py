# model_clients/gemini_client.py
from __future__ import annotations
from typing import List, Dict, Tuple
from google import genai
from google.genai import types
from .base import BaseModelClient


class GeminiModelClient(BaseModelClient):
    def __init__(self, model: str, api_key: str):
        self._model = model
        self._client = genai.Client(api_key=api_key)

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
    ) -> Tuple[str, int, int]:
        # Flatten messages into a single textual history
        history_str = "\n".join(f"{m['role']}: {m['content']}" for m in messages)

        response = self._client.models.generate_content(
            model=self._model,
            contents=history_str,
            config=types.GenerateContentConfig(
                system_instruction="",
                temperature=temperature,
            ),
        )

        text = response.text

        # usage metadata is available
        usage_meta = response.usage_metadata
        prompt_tokens = getattr(usage_meta, "prompt_token_count", 0)
        completion_tokens = getattr(usage_meta, "candidates_token_count", 0)

        return text, prompt_tokens, completion_tokens

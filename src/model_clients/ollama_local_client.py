from __future__ import annotations
from typing import List, Dict, Tuple
import asyncio
import time
import ollama

from .base import BaseModelClient


class OllamaLocalModelClient(BaseModelClient):
    """
    Local Ollama client using the official `ollama` Python package.
    This wraps the *exact* logic you already trust.
    """
    

    def __init__(
        self,
        model: str,
        keep_alive: str | None = None,
        options: Dict | None = None,
    ):
        self._model = model
        self._keep_alive = keep_alive
        self._options = options or {}

    # --------------------------------------------------
    # Internal sync call (your proven logic)
    # --------------------------------------------------
    def _run_sync(self, messages: List[Dict[str, str]], temperature: float):
        start = time.time()

        response = ollama.chat(
            model=self._model,
            messages=messages,
            keep_alive=self._keep_alive,
            options={
                **self._options,
                "temperature": temperature,
            },
        )

        text = response["message"]["content"]

        # Token counts (best-effort; Ollama provides these in recent versions)
        prompt_tokens = response.get("prompt_eval_count", 0)
        completion_tokens = response.get("eval_count", 0)

        latency = time.time() - start
        return text, prompt_tokens, completion_tokens, latency

    # --------------------------------------------------
    # BaseModelClient API (async)
    # --------------------------------------------------
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
    ) -> Tuple[str, int, int]:

        try:
            text, prompt_tokens, completion_tokens, _ = await asyncio.to_thread(
                self._run_sync, messages, temperature
            )
            return text, prompt_tokens, completion_tokens

        except ollama.ResponseError as e:
            raise RuntimeError(
                f"Ollama ResponseError [{e.status_code}]: {e.error}"
            ) from e

        except Exception as e:
            raise RuntimeError(
                f"Ollama unexpected error: {e}"
            ) from e

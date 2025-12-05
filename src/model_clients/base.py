# model_clients/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class BaseModelClient(ABC):
    """
    Unified interface for all LLM providers.

    All implementations must:
      - accept a list of {"role": ..., "content": ...} messages
      - return (text, prompt_tokens, completion_tokens)
    """

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
    ) -> Tuple[str, int, int]:
        """
        :param messages: Chat history in OpenAI-style format.
        :param temperature: Sampling temperature.
        :return: (text, prompt_tokens, completion_tokens)
        """
        raise NotImplementedError

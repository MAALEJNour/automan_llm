from typing import AsyncGenerator, Sequence, List, Dict
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, TextMessage
from autogen_core import CancellationToken
from autogen_core.model_context import UnboundedChatCompletionContext
from autogen_core.models import AssistantMessage, RequestUsage, UserMessage, SystemMessage
from model_clients.base import BaseModelClient


class LLMAssistantAgent(BaseChatAgent):
    """
    Generic assistant agent for AutoGen that uses any model client
    implementing BaseModelClient.
    """

    def __init__(
        self,
        name: str,
        model_client: BaseModelClient,
        description: str = "Generic AutoGen LLM Agent",
        system_message: str = "You are a helpful assistant.",
        temperature: float = 0.0,
    ):
        super().__init__(name=name, description=description)
        self._model_client = model_client
        self._system_message = system_message
        self._temperature = temperature

        # memory
        self._ctx = UnboundedChatCompletionContext()

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        return (TextMessage,)

    # =========================
    # AutoGen ENTRY POINT
    # =========================
    async def on_messages(
        self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        final = None
        async for m in self.on_messages_stream(messages, cancellation_token):
            if isinstance(m, Response):
                final = m
        if final is None:
            raise AssertionError("LLMAssistantAgent must return a Response.")
        return final

    # =========================
    # STREAMING LOGIC
    # =========================
    async def on_messages_stream(
        self,
        messages: Sequence[BaseChatMessage],
        cancellation_token: CancellationToken
    ) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | Response, None]:

        # 1. Add incoming messages to memory
        for msg in messages:
            await self._ctx.add_message(msg.to_model_message())

        # 2. Build API-ready message format
        history: List[Dict[str, str]] = [{"role": "system", "content": self._system_message}]
        for m in await self._ctx.get_messages():
            if isinstance(m, UserMessage):
                role = "user"
            elif isinstance(m, AssistantMessage):
                role = "assistant"
            elif isinstance(m, SystemMessage):
                role = "system"
            else:
                role = "user"

            history.append({"role": role, "content": m.content})

        # 3. Call underlying model API through BaseModelClient
        text, prompt_tokens, completion_tokens = await self._model_client.generate(
            messages=history,
            temperature=self._temperature
        )

        # 4. Build AutoGen usage structure
        usage = RequestUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens
        )

        # 5. Add to memory
        await self._ctx.add_message(AssistantMessage(content=text, source=self.name))

        # 6. Return final AutoGen Response
        yield Response(
            chat_message=TextMessage(
                content=text,
                source=self.name,
                models_usage=usage
            ),
            inner_messages=[]
        )

    # =========================
    # RESET
    # =========================
    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        await self._ctx.clear()

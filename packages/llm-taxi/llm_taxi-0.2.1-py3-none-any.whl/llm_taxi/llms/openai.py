from collections.abc import AsyncGenerator
from typing import Any, ClassVar

from llm_taxi.conversation import Message
from llm_taxi.llms import LLM


class OpenAI(LLM):
    env_vars: ClassVar[dict[str, str]] = {
        "api_key": "OPENAI_API_KEY",
    }

    def _init_client(self, **kwargs) -> Any:
        from openai import AsyncClient

        return AsyncClient(**kwargs)

    async def _streaming_response(self, response: Any) -> AsyncGenerator:
        async for chunk in response:
            if content := chunk.choices[0].delta.content:
                yield content

    async def streaming_response(
        self,
        messages: list[Message],
        **kwargs,
    ) -> AsyncGenerator:
        messages = self._convert_messages(messages)

        response = await self.client.chat.completions.create(
            messages=messages,
            stream=True,
            **self._get_call_kwargs(**kwargs),
        )

        return self._streaming_response(response)

    async def response(self, messages: list[Message], **kwargs) -> str:
        messages = self._convert_messages(messages)

        response = await self.client.chat.completions.create(
            messages=messages,
            **self._get_call_kwargs(**kwargs),
        )

        if content := response.choices[0].message.content:
            return content

        return ""

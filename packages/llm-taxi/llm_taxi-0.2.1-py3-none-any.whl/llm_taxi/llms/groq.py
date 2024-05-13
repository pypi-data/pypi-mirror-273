from typing import Any, ClassVar

from groq import AsyncGroq
from groq.types.chat.completion_create_params import Message as GroqMessage

from llm_taxi.conversation import Message
from llm_taxi.llms.openai import OpenAI


class Groq(OpenAI):
    env_vars: ClassVar[dict[str, str]] = {
        "api_key": "GROQ_API_KEY",
    }

    def _init_client(self, **kwargs) -> Any:
        return AsyncGroq(**kwargs)

    def _convert_messages(self, messages: list[Message]) -> list[Any]:
        return [
            GroqMessage(
                role=message.role.value,
                content=message.content,
            )
            for message in messages
        ]

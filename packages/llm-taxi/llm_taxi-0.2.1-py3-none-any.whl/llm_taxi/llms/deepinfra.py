from typing import ClassVar

from llm_taxi.llms.openai import OpenAI


class DeepInfra(OpenAI):
    env_vars: ClassVar[dict[str, str]] = {
        "api_key": "DEEPINFRA_API_KEY",
        "base_url": "DEEPINFRA_BASE_URL",
    }

import os
from collections.abc import Mapping

from llm_taxi.llms import (
    LLM,
    Anthropic,
    DashScope,
    DeepInfra,
    DeepSeek,
    Google,
    Groq,
    Mistral,
    OpenAI,
    OpenRouter,
    Perplexity,
    Together,
)

MODEL_CLASSES: Mapping[str, type[LLM]] = {
    "openai": OpenAI,
    "google": Google,
    "together": Together,
    "groq": Groq,
    "anthropic": Anthropic,
    "mistral": Mistral,
    "perplexity": Perplexity,
    "deepinfra": DeepInfra,
    "deepseek": DeepSeek,
    "openrouter": OpenRouter,
    "dashscope": DashScope,
}


def _get_env(key: str) -> str:
    if (value := os.getenv(key)) is None:
        msg = f"Required environment variable `{key}` not found"
        raise KeyError(msg)

    return value


def llm(
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
    call_kwargs: dict | None = None,
    **client_kwargs,
) -> LLM:
    provider, model = model.split(":", 1)
    if not (model_class := MODEL_CLASSES.get(provider)):
        msg = f"Unknown LLM provider: {provider}"
        raise ValueError(msg)

    env_var_values: dict[str, str] = {}
    for key, env_name in model_class.env_vars.items():
        value = (
            params if (params := locals().get(key)) is not None else _get_env(env_name)
        )
        env_var_values[key] = value

    return model_class(
        model=model,
        **env_var_values,
        call_kwargs=call_kwargs,
        **client_kwargs,
    )

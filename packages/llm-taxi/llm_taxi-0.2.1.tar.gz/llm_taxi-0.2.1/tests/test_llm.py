import asyncio
import copy

from llm_taxi.conversation import Message, Role
from llm_taxi.factory import llm


async def main():
    clients = [
        llm(model="openai:gpt-3.5-turbo"),
        llm(model="google:gemini-pro"),
        llm(model="together:meta-llama/Llama-3-70b-chat-hf"),
        llm(model="groq:llama3-70b-8192"),
        llm(model="anthropic:claude-2.1"),
        llm(model="mistral:mistral-small"),
        llm(model="perplexity:llama-3-8b-instruct"),
        llm(model="deepinfra:meta-llama/Meta-Llama-3-8B-Instruct"),
        llm(model="deepseek:deepseek-chat"),
        llm(model="openrouter:rwkv/rwkv-5-world-3b"),
        llm(model="dashscope:qwen-turbo"),
    ]

    for client in clients:
        print(client.model)
        copy.deepcopy(client)

        messages = [
            Message(role=Role.User, content="What is the capital of France?"),
        ]
        response = await client.response(messages)
        print(response)

        response = await client.streaming_response(messages)
        async for chunk in response:
            print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())

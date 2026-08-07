"""Chapter 01: the smallest LangChain conversation."""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


def build_model() -> ChatOpenAI:
    load_dotenv(Path(__file__).parents[2] / ".env")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    if not api_key or not model:
        raise RuntimeError("请复制 .env.example 为 .env，并配置 LLM_API_KEY 和 LLM_MODEL")
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        base_url=os.getenv("LLM_BASE_URL") or None,
        timeout=float(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
        temperature=0,
    )


def main() -> None:
    messages = [
        SystemMessage(content="你是 AI Agent 面试官，回答必须简洁准确。"),
        HumanMessage(content="Agent 和普通 LLM 调用最核心的区别是什么？"),
    ]
    answer = build_model().invoke(messages)
    print("消息类型:", [message.type for message in messages])
    print("模型回答:", answer.content)
    if answer.usage_metadata:
        print("Token 使用:", answer.usage_metadata)


if __name__ == "__main__":
    main()

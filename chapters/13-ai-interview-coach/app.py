"""CLI entry point for the complete interview coach."""

import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.types import Command

from domain import InterviewState
from knowledge import KnowledgeBase, load_chunks
from workflow import build_workflow


def load_components():
    root = Path(__file__).parents[2]
    load_dotenv(root / ".env")
    api_key = os.getenv("LLM_API_KEY")
    model_name = os.getenv("LLM_MODEL")
    if not api_key or not model_name:
        raise RuntimeError("请配置 LLM_API_KEY 和 LLM_MODEL")
    common = {"api_key": api_key, "base_url": os.getenv("LLM_BASE_URL") or None}
    model = ChatOpenAI(model=model_name, temperature=0, **common)
    embeddings = OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"), **common
    )
    material_root = root / "materials" / "ai-agent-book" / "book"
    return model, KnowledgeBase(load_chunks(material_root), embeddings)


def main() -> None:
    model, knowledge = load_components()
    graph = build_workflow(model, knowledge)
    topic = input("面试主题 [RAG]：").strip() or "RAG"
    initial: InterviewState = {
        "topic": topic,
        "max_questions": 3,
        "question_index": 0,
        "results": [],
    }
    config = {"configurable": {"thread_id": str(uuid4())}}
    state = graph.invoke(initial, config)
    while state.get("__interrupt__"):
        request = state["__interrupt__"][0].value
        print(f"\n第 {request['index']} 题：{request['question']}")
        answer = input("你的回答：")
        state = graph.invoke(Command(resume=answer), config)
    print("\n面试报告\n" + state["report"])


if __name__ == "__main__":
    main()

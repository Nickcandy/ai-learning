"""Chapter 06: retrieve chunks and answer only with cited evidence."""

import os
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def load_chapter05():
    path = Path(__file__).parents[1] / "05-rag-data-preparation" / "main.py"
    spec = spec_from_file_location("chapter05", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载第 05 章")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def format_context(documents: list[Document]) -> str:
    return "\n\n".join(
        f"[{doc.metadata['chunk_id']}] source={doc.metadata['source']}\n{doc.page_content}"
        for doc in documents
    )


def main() -> None:
    root = Path(__file__).parents[2]
    load_dotenv(root / ".env")
    api_key = os.getenv("LLM_API_KEY")
    model_name = os.getenv("LLM_MODEL")
    if not api_key or not model_name:
        raise RuntimeError("请配置 LLM_API_KEY 和 LLM_MODEL")
    chapter05 = load_chapter05()
    source = root / "materials" / "ai-agent-book" / "book"
    chunks = chapter05.split_documents(chapter05.load_markdown_documents(source, limit=2))[:30]
    embeddings = OpenAIEmbeddings(
        api_key=api_key,
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        base_url=os.getenv("LLM_BASE_URL") or None,
    )
    store = InMemoryVectorStore.from_documents(chunks, embeddings)
    question = "Tool Calling 的执行循环是怎样的？"
    matches = store.similarity_search(question, k=4)
    context = format_context(matches)
    model = ChatOpenAI(
        api_key=api_key,
        model=model_name,
        base_url=os.getenv("LLM_BASE_URL") or None,
        temperature=0,
    )
    answer = model.invoke(
        [
            SystemMessage(content="只根据资料回答。每个结论引用 [chunk_id]；资料不足时明确说不知道。"),
            HumanMessage(content=f"问题：{question}\n\n资料：\n{context}"),
        ]
    )
    print(answer.content)
    print("\n召回来源:")
    for doc in matches:
        print(doc.metadata)


if __name__ == "__main__":
    main()

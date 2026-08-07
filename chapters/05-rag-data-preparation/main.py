"""Chapter 05: load Markdown and create traceable chunks."""

from pathlib import Path

from langchain.messages import HumanMessage
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_markdown_documents(root: Path, limit: int = 3) -> list[Document]:
    paths = sorted(root.glob("*.md"))[:limit]
    if not paths:
        raise FileNotFoundError(f"没有在 {root} 找到 Markdown 资料")
    return [
        Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": str(path)})
        for path in paths
    ]


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(documents)
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk-{index:04d}"
    return chunks


def main() -> None:
    root = Path(__file__).parents[2] / "materials" / "ai-agent-book" / "book"
    documents = load_markdown_documents(root)
    chunks = split_documents(documents)
    print(f"documents={len(documents)}, chunks={len(chunks)}")
    sample = chunks[0]
    print("metadata=", sample.metadata)
    print("content=", sample.page_content[:300].replace("\n", " "))


if __name__ == "__main__":
    main()

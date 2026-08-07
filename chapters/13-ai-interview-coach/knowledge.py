"""Build and query the interview knowledge base."""

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_chunks(root: Path, max_files: int = 5) -> list[Document]:
    paths = sorted(root.glob("*.md"))[:max_files]
    if not paths:
        raise FileNotFoundError(f"没有在 {root} 找到 Markdown 资料")
    documents = [
        Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": str(path)})
        for path in paths
    ]
    chunks = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120).split_documents(documents)
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"kb-{index:04d}"
    return chunks


class KnowledgeBase:
    def __init__(self, chunks: list[Document], embeddings: Embeddings) -> None:
        self.store = InMemoryVectorStore.from_documents(chunks, embeddings)

    def search(self, query: str, k: int = 4) -> list[Document]:
        if not query.strip():
            raise ValueError("检索问题不能为空")
        return self.store.similarity_search(query, k=k)


def format_evidence(documents: list[Document]) -> str:
    return "\n\n".join(
        f"[{doc.metadata['chunk_id']}] source={doc.metadata['source']}\n{doc.page_content}"
        for doc in documents
    )

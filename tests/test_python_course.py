from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from langchain_core.documents import Document


ROOT = Path(__file__).parents[1]


def load_chapter(directory: str):
    path = ROOT / "chapters" / directory / "main.py"
    spec = spec_from_file_location(directory, path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_chunks_keep_source_and_get_id() -> None:
    chapter = load_chapter("05-rag-data-preparation")
    chunks = chapter.split_documents([Document(page_content="Agent " * 500, metadata={"source": "demo.md"})])
    assert len(chunks) > 1
    assert chunks[0].metadata == {"source": "demo.md", "chunk_id": "chunk-0000"}


def test_context_contains_citation_ids() -> None:
    chapter = load_chapter("06-retrieval-and-citations")
    context = chapter.format_context(
        [Document(page_content="evidence", metadata={"source": "demo.md", "chunk_id": "chunk-0001"})]
    )
    assert "[chunk-0001]" in context
    assert "source=demo.md" in context


def test_rag_metrics() -> None:
    chapter = load_chapter("07-rag-evaluation")
    assert chapter.recall_at_k({"a", "b"}, ["a", "x"], 2) == 0.5
    assert chapter.reciprocal_rank({"b"}, ["a", "b"]) == 0.5


def test_workflow_reaches_completion() -> None:
    chapter = load_chapter("08-langgraph-workflow")
    result = chapter.build_graph().invoke(
        {"topic": "RAG", "question_index": 0, "max_questions": 2, "current_question": "", "status": "asking"}
    )
    assert result["status"] == "completed"
    assert result["question_index"] == 2

import sys
from pathlib import Path

from langchain_core.documents import Document


CHAPTER = Path(__file__).parents[1] / "chapters" / "13-ai-interview-coach"
sys.path.insert(0, str(CHAPTER))

from domain import build_report  # noqa: E402
from knowledge import format_evidence  # noqa: E402


def test_report_uses_deterministic_average() -> None:
    report = build_report(
        "RAG",
        [
            {"score": 80, "feedback": "召回解释准确"},
            {"score": 60, "feedback": "缺少评测"},
        ],
    )
    assert "平均分 70.0" in report
    assert "缺少评测" in report


def test_evidence_keeps_source_and_chunk_id() -> None:
    evidence = format_evidence(
        [Document(page_content="evidence", metadata={"source": "chapter.md", "chunk_id": "kb-0001"})]
    )
    assert "[kb-0001]" in evidence
    assert "source=chapter.md" in evidence

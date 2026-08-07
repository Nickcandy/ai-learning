"""Chapter 07: deterministic retrieval metrics."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvalCase:
    question: str
    relevant_ids: set[str]
    retrieved_ids: list[str]


def recall_at_k(relevant_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if not relevant_ids:
        raise ValueError("relevant_ids 不能为空")
    hits = relevant_ids.intersection(retrieved_ids[:k])
    return len(hits) / len(relevant_ids)


def reciprocal_rank(relevant_ids: set[str], retrieved_ids: list[str]) -> float:
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_ids:
            return 1 / rank
    return 0.0


def evaluate(cases: list[EvalCase], k: int = 3) -> dict[str, float]:
    if not cases:
        raise ValueError("评测集不能为空")
    recalls = [recall_at_k(case.relevant_ids, case.retrieved_ids, k) for case in cases]
    ranks = [reciprocal_rank(case.relevant_ids, case.retrieved_ids) for case in cases]
    return {"recall_at_k": sum(recalls) / len(recalls), "mrr": sum(ranks) / len(ranks)}


def main() -> None:
    cases = [
        EvalCase("什么是 Tool Calling？", {"chunk-0012"}, ["chunk-0012", "chunk-0008"]),
        EvalCase("Checkpoint 有什么作用？", {"chunk-0031"}, ["chunk-0010", "chunk-0031"]),
    ]
    print(evaluate(cases))


if __name__ == "__main__":
    main()

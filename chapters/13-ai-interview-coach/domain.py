"""Typed contracts shared by the interview workflow."""

from typing import NotRequired, TypedDict

from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):
    question: str = Field(min_length=10)
    expected_points: list[str] = Field(min_length=2, max_length=5)


class AnswerScore(BaseModel):
    score: int = Field(ge=0, le=100)
    strengths: list[str] = Field(default_factory=list, max_length=5)
    missing_points: list[str] = Field(default_factory=list, max_length=5)
    feedback: str = Field(min_length=1)


class InterviewState(TypedDict):
    topic: str
    max_questions: int
    question_index: int
    results: list[dict[str, object]]
    current_question: NotRequired[str]
    expected_points: NotRequired[list[str]]
    evidence: NotRequired[str]
    answer: NotRequired[str]
    report: NotRequired[str]


def build_report(topic: str, results: list[dict[str, object]]) -> str:
    if not results:
        return f"{topic} 面试没有完成任何题目。"
    scores = [int(result["score"]) for result in results]
    lines = [f"{topic} 面试完成：{len(results)} 题，平均分 {sum(scores) / len(scores):.1f}。"]
    for index, result in enumerate(results, start=1):
        lines.append(f"第 {index} 题 {result['score']} 分：{result['feedback']}")
    return "\n".join(lines)

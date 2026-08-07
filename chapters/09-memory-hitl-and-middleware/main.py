"""Chapter 09: checkpoint an interrupted workflow and resume it."""

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class ReviewState(TypedDict):
    answer: str
    approved: bool
    feedback: str


def human_review(state: ReviewState) -> dict[str, object]:
    decision = interrupt({"answer": state["answer"], "question": "是否接受这份面试评分？"})
    if not isinstance(decision, dict) or not isinstance(decision.get("approved"), bool):
        raise ValueError("恢复数据必须包含 approved: bool")
    return {"approved": decision["approved"], "feedback": str(decision.get("feedback", ""))}


def build_graph():
    builder = StateGraph(ReviewState)
    builder.add_node("human_review", human_review)
    builder.add_edge(START, "human_review")
    builder.add_edge("human_review", END)
    return builder.compile(checkpointer=InMemorySaver())


def main() -> None:
    graph = build_graph()
    config = {"configurable": {"thread_id": "demo-interview-1"}}
    initial: ReviewState = {"answer": "RAG 通过外部检索补充模型上下文。", "approved": False, "feedback": ""}
    interrupted = graph.invoke(initial, config)
    print("中断状态:", interrupted)
    resumed = graph.invoke(Command(resume={"approved": True, "feedback": "解释准确"}), config)
    print("恢复结果:", resumed)


if __name__ == "__main__":
    main()

"""Chapter 08: a deterministic interview workflow."""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class InterviewState(TypedDict):
    topic: str
    question_index: int
    max_questions: int
    current_question: str
    status: Literal["asking", "completed"]


def create_question(state: InterviewState) -> dict[str, object]:
    index = state["question_index"] + 1
    return {
        "question_index": index,
        "current_question": f"第 {index} 题：请解释 {state['topic']} 的核心设计。",
        "status": "asking",
    }


def advance(state: InterviewState) -> dict[str, str]:
    status = "completed" if state["question_index"] >= state["max_questions"] else "asking"
    return {"status": status}


def route(state: InterviewState) -> Literal["create_question", "__end__"]:
    return END if state["status"] == "completed" else "create_question"


def build_graph():
    builder = StateGraph(InterviewState)
    builder.add_node("create_question", create_question)
    builder.add_node("advance", advance)
    builder.add_edge(START, "create_question")
    builder.add_edge("create_question", "advance")
    builder.add_conditional_edges("advance", route)
    return builder.compile()


def main() -> None:
    initial: InterviewState = {
        "topic": "RAG",
        "question_index": 0,
        "max_questions": 3,
        "current_question": "",
        "status": "asking",
    }
    print(build_graph().invoke(initial))


if __name__ == "__main__":
    main()

"""LangGraph workflow for a resumable interview session."""

from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from domain import AnswerScore, InterviewQuestion, InterviewState, build_report
from knowledge import KnowledgeBase, format_evidence


def build_workflow(model: ChatOpenAI, knowledge: KnowledgeBase):
    question_model = model.with_structured_output(InterviewQuestion)
    score_model = model.with_structured_output(AnswerScore)

    def prepare_question(state: InterviewState) -> dict[str, object]:
        documents = knowledge.search(f"{state['topic']} AI Agent 面试知识点", k=4)
        evidence = format_evidence(documents)
        question = question_model.invoke(
            [
                SystemMessage(content="只根据资料生成一道有区分度的技术面试题。"),
                HumanMessage(
                    content=(
                        f"主题：{state['topic']}\n"
                        f"这是第 {state['question_index'] + 1} 题。\n资料：\n{evidence}"
                    )
                ),
            ]
        )
        return {
            "question_index": state["question_index"] + 1,
            "current_question": question.question,
            "expected_points": question.expected_points,
            "evidence": evidence,
        }

    def wait_for_answer(state: InterviewState) -> dict[str, str]:
        answer = interrupt(
            {"index": state["question_index"], "question": state["current_question"]}
        )
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("面试回答不能为空")
        return {"answer": answer.strip()}

    def score_answer(state: InterviewState) -> dict[str, object]:
        score = score_model.invoke(
            [
                SystemMessage(content="根据资料和预期要点评分。不要因为表达风格扣分。"),
                HumanMessage(
                    content=(
                        f"问题：{state['current_question']}\n"
                        f"预期要点：{state['expected_points']}\n"
                        f"候选人回答：{state['answer']}\n"
                        f"资料：\n{state['evidence']}"
                    )
                ),
            ]
        )
        result = score.model_dump()
        result["question"] = state["current_question"]
        return {"results": [*state["results"], result]}

    def finish(state: InterviewState) -> dict[str, str]:
        return {"report": build_report(state["topic"], state["results"])}

    def route(state: InterviewState) -> str:
        return "finish" if state["question_index"] >= state["max_questions"] else "prepare_question"

    builder = StateGraph(InterviewState)
    builder.add_node("prepare_question", prepare_question)
    builder.add_node("wait_for_answer", wait_for_answer)
    builder.add_node("score_answer", score_answer)
    builder.add_node("finish", finish)
    builder.add_edge(START, "prepare_question")
    builder.add_edge("prepare_question", "wait_for_answer")
    builder.add_edge("wait_for_answer", "score_answer")
    builder.add_conditional_edges("score_answer", route)
    builder.add_edge("finish", END)
    return builder.compile(checkpointer=InMemorySaver())

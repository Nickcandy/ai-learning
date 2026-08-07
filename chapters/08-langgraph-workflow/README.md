# 08 LangGraph StateGraph

本章故意不调用模型，只学习状态与控制流。确定性业务规则应写成普通节点和条件边，不要交给 LLM 猜测。

```bash
uv run python chapters/08-langgraph-workflow/main.py
```

```text
START -> create_question -> advance -> route
                    ^                    |
                    +------ asking ------+
                              |
                          completed -> END
```

State 是节点之间唯一共享的数据契约。节点返回局部更新，条件边决定下一步。图必须存在明确终止条件。

## 面试题

**LangChain Agent 和 LangGraph 是什么关系？** 当前 LangChain Agent 构建在 LangGraph 上；前者提供常用 Agent Harness，后者提供低层状态编排和持久化。

**所有流程都适合 Graph 吗？** 否。单次模型调用或简单线性 Pipeline 使用普通函数更清晰。

官方资料：[LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)。

# 03 Tools 与 Agent Loop

工具不是模型内部能力。模型只生成调用请求，应用验证参数、执行本地函数，再把结果作为 `ToolMessage` 送回模型。

```bash
uv run python chapters/03-tools-and-agent-loop/main.py
```

## 核心循环

```text
HumanMessage -> Model -> AIMessage(tool_calls)
    -> Tool -> ToolMessage -> Model -> AIMessage(final answer)
```

`@tool` 根据函数名、类型和 docstring 生成 Schema。只有显式注册的函数才允许执行；永远不要把模型参数直接拼成 Shell 或 SQL。

## 面试题

**模型调用工具时，模型真的执行了函数吗？** 没有。模型只生成结构化意图，执行发生在应用进程。

**为什么需要最大循环次数？** 工具结果可能持续诱发新调用，没有上限会造成无限循环和费用失控。

**工具失败应该怎么处理？** 根据业务选择终止或把明确错误作为 ToolMessage 返回模型；不能吞错。

官方资料：[Tools](https://docs.langchain.com/oss/python/langchain/tools)、[Agents](https://docs.langchain.com/oss/python/langchain/agents)。

# AI Learning

这是一个面向 AI Agent 学习和面试准备的可运行课程仓库。课程代码以当前官方文档为基准：先用 LangChain/LangGraph 学习核心概念，再用 Go/Eino 重建关键能力，最后完成 AI Agent 面试教练。

## 学习方式

你不需要补全代码。每章都提供完整示例、运行命令、执行流程、常见风险和面试问答。建议按顺序阅读：

1. 先读本章 `README.md`，预测程序会如何执行。
2. 运行代码，观察模型消息、工具调用和状态变化。
3. 不看答案口头回答面试题，再核对参考要点。

仓库中的少量测试用于保证关键算法和数据流没有被改坏，不是学习任务。

## 课程路线

完整章节与验收标准见 [COURSE.md](COURSE.md)。

```text
LangChain 基础 -> Tool Calling -> RAG -> LangGraph -> Memory/HITL
    -> Middleware/Evaluation -> Eino -> AI Agent 面试教练
```

## 环境

Python 章节需要 Python 3.11+：

```bash
uv sync
cp .env.example .env
uv run python chapters/01-model-and-messages/main.py
uv run pytest -q
```

Go/Eino 章节需要 Go 1.24+：

```bash
go mod download
go run ./chapters/10-eino-model-and-messages
go test ./...
```

`.env` 使用 OpenAI Chat Completions 兼容接口。`materials/ai-agent-book` 是本地参考资料，不会提交到主仓库。

## 官方资料

- [LangChain](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [Eino](https://www.cloudwego.io/docs/eino/)

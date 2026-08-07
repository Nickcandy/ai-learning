# 04 Streaming 与 Trace

最终回答不能解释 Agent 为什么成功或失败。本章使用 `updates` 流观察模型节点和工具节点的增量状态。

```bash
uv run python chapters/04-streaming-and-tracing/main.py
```

## 需要区分的三个概念

- Token Streaming：尽快展示生成中的文本。
- State Streaming：展示每个节点对状态的更新。
- Tracing：持久记录输入、输出、延迟、Token、错误和父子调用关系。

生产系统应给一次任务分配稳定的 trace ID，并避免把 API Key、隐私数据和完整内部文档写入日志。

## 面试题

**为什么只有普通日志不够？** Agent 一次请求包含多次模型与工具调用，需要父子关系才能定位成本和失败节点。

**Streaming 会减少总耗时吗？** 通常不会减少完整生成耗时，但会改善首 Token 延迟和用户感知。

官方资料：[Streaming](https://docs.langchain.com/oss/python/langchain/streaming)、[Observability](https://docs.langchain.com/oss/python/langchain/observability)。

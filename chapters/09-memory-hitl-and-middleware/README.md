# 09 Memory、HITL 与 Middleware

本章演示 `interrupt` 暂停图、Checkpoint 保存状态，以及用同一个 `thread_id` 恢复。`middleware.py` 展示工具错误如何转换为对模型可见的 `ToolMessage`。

```bash
uv run python chapters/09-memory-hitl-and-middleware/main.py
```

## 边界

- 短期 Memory 保存当前线程状态，不等于长期用户画像。
- `InMemorySaver` 只适合学习和测试；进程退出后数据消失。
- HITL 不只是弹窗，必须包含稳定任务 ID、权限检查、过期策略和幂等恢复。
- Middleware 适合日志、重试、Guardrail 和工具策略，不应隐藏核心业务流程。

## 面试题

**Checkpoint 和聊天历史有什么区别？** 聊天历史只是状态的一部分；Checkpoint 还保存节点位置、业务字段和恢复所需元数据。

**为什么恢复操作要幂等？** 网络重试可能重复提交审批，非幂等实现会造成工具或外部操作重复执行。

官方资料：[Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)、[Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)、[Middleware](https://docs.langchain.com/oss/python/langchain/middleware/overview)。

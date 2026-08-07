# 13 AI Agent 面试教练

这是课程最终项目。它把向量 RAG、Structured Output、LangGraph、Interrupt、Checkpoint 和确定性报告组合成三题面试流程。

```bash
uv run python chapters/13-ai-interview-coach/app.py
```

## 模块边界

- `domain.py`：输入输出 Schema、Graph State 和确定性报告。
- `knowledge.py`：资料加载、Chunk、向量索引、召回和引用格式。
- `workflow.py`：出题、等待回答、评分、循环和结束条件。
- `app.py`：环境配置与 CLI 交互。

## 完整数据流

```text
topic -> retrieve -> structured question -> interrupt
  -> user answer -> structured score -> route
  -> next question / deterministic report
```

## 生产化差距

当前使用 `InMemoryVectorStore` 和 `InMemorySaver`，重启后索引与会话都会消失。生产版本还需要持久向量库、数据库 Checkpointer、身份认证、文档权限过滤、限流、重试、评测流水线和敏感信息脱敏。这些不是示例中可以假装已经解决的问题。

## 面试题

**为什么报告使用确定性代码而不是再调用一次模型？** 分数聚合不需要生成能力；普通代码更便宜、稳定且可测试。

**为什么检索放在每道题之前？** 不同题目需要独立证据集合，同时便于记录该题的召回轨迹和引用。

**这个系统首先应该优化什么指标？** 先保证检索命中和评分依据正确，再优化回答风格；错误证据会系统性污染后续生成。

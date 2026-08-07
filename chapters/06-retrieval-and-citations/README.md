# 06 Retrieval 与引用

本章形成最小 RAG：Embedding、向量索引、Top-K 召回、上下文组装和带引用回答。

```bash
uv run python chapters/06-retrieval-and-citations/main.py
```

## 数据流

```text
Chunks -> Embeddings -> Vector Store
Question -> Query Embedding -> Top-K -> Context -> LLM -> Cited Answer
```

向量相似只表示语义接近，不表示内容真实或足以回答。应用必须把召回来源一起记录，并要求资料不足时拒答。

## 面试题

**Top-K 越大越好吗？** 否。K 太大会增加费用、延迟和噪声，甚至让真正证据被淹没。

**为什么引用不能只靠模型生成？** 模型可能伪造 ID；生产系统还应解析引用并检查 ID 是否来自本轮召回集合。

官方资料：[Eino Retriever](https://www.cloudwego.io/docs/eino/core_modules/components/retriever_guide/)。

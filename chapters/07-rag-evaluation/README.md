# 07 RAG Evaluation

没有评测集，就无法判断换 Chunk、Embedding 或 Top-K 后系统是否真的变好。本章完全离线，计算 Recall@K 和 MRR。

```bash
uv run python chapters/07-rag-evaluation/main.py
```

- Recall@K：相关 Chunk 有多少进入前 K。
- MRR：第一个相关 Chunk 出现得有多靠前。

检索指标只评价“找到了什么”，还需单独评价答案正确性、引用一致性、延迟和成本。评测集应来自真实问题，并由人标注相关 Chunk。

## 面试题

**为什么不能只让另一个 LLM 判断回答好不好？** LLM Judge 也有偏差和漂移，应与确定性指标、人工抽检和固定版本共同使用。

**离线指标提高是否保证线上效果提高？** 不保证。线上问题分布、权限过滤和延迟约束可能不同。

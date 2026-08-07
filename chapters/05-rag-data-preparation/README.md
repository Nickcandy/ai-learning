# 05 RAG 数据准备

RAG 的第一步不是向量数据库，而是把原始资料转换为带来源信息的 Chunk。

```bash
uv run python chapters/05-rag-data-preparation/main.py
```

## 数据流

```text
Markdown -> Document(source) -> Text Splitter -> Chunk(source, chunk_id)
```

`chunk_size` 太大会混入多个主题，太小会丢失上下文；`chunk_overlap` 能减少边界信息丢失，但会增加索引体积和重复召回。示例保留 `source` 和 `chunk_id`，为后续引用与评测提供依据。

## 面试题

**Chunk 大小如何选择？** 根据文档结构、问题粒度、Embedding 模型和实验数据决定，不存在通用最佳值。

**为什么 Metadata 很重要？** 过滤、权限、去重、引用和线上问题定位都依赖它。

官方资料：[Retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval)、[Eino Document Transformer](https://www.cloudwego.io/docs/eino/core_modules/components/document_transformer_guide/)。

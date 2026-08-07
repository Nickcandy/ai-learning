# 11 Eino RAG 与 Graph

本章实现一个离线 `retriever.Retriever`，并通过 `AddRetrieverNode` 接入 Eino Graph。关键词检索只是为了让测试完全离线；生产版本可以替换为向量检索而不改变 Graph 的输入输出类型。

```bash
go run ./chapters/11-eino-rag-and-graph
go test ./chapters/11-eino-rag-and-graph
```

```text
string query -> Retriever -> []*schema.Document -> Lambda formatter -> string
```

## 面试题

**Eino Component 的价值是什么？** Loader、Transformer、Embedding、Indexer、Retriever 和 ChatModel 通过稳定接口组合，业务图不依赖具体供应商实现。

**为什么自定义 Retriever 仍要返回 Document Metadata？** 来源、分数、权限和索引信息需要沿 Pipeline 传播。

官方资料：[Retriever](https://www.cloudwego.io/docs/eino/core_modules/components/retriever_guide/)、[Chain/Graph](https://www.cloudwego.io/docs/eino/core_modules/chain_and_graph_orchestration/)。

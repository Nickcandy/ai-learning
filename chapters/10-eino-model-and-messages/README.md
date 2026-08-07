# 10 Eino Model 与 Messages

本章把第 01 章映射到 Go/Eino：`openai.ChatModel` 对应模型组件，`schema.Message` 是组件之间的统一消息协议。

```bash
go run ./chapters/10-eino-model-and-messages
```

## 对照

| LangChain | Eino |
|---|---|
| `ChatOpenAI` | `openai.ChatModel` |
| `SystemMessage` | `schema.SystemMessage` |
| `HumanMessage` | `schema.UserMessage` |
| `invoke` | `Generate` |

Go 版本显式传播 `context.Context`，超时会取消等待中的请求；所有构造和调用错误都向上返回。

## 面试题

**为什么 Context 应从入口一直传到模型和工具？** 请求取消、Deadline 和 Trace 信息需要跨组件传播；重新创建 Background 会切断这条链路。

官方资料：[Eino ChatModel](https://www.cloudwego.io/docs/eino/core_modules/components/chat_model_guide/)、[Quick Start Chapter 1](https://www.cloudwego.io/docs/eino/quick_start/chapter_01_chatmodel_and_message/)。

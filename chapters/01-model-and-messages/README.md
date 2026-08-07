# 01 Model 与 Messages

本章对应 LangChain 官方的 Models 与 Messages。目标不是记住 `ChatOpenAI`，而是理解一次调用的输入、输出和配置边界。

## 运行

```bash
uv run python chapters/01-model-and-messages/main.py
```

## 数据流

```text
.env -> ChatOpenAI -> [SystemMessage, HumanMessage] -> AIMessage
```

`SystemMessage` 定义长期行为，`HumanMessage` 表示本轮用户输入，模型返回 `AIMessage`。`temperature=0` 只能降低随机性，不能保证事实正确。

## 阅读重点

- API Key、模型名、Base URL 和超时属于运行配置，不应硬编码。
- Message 不只是字符串，它还可能携带工具调用、内容块和 Token 元数据。
- 调用失败会直接抛错；示例不会把网络错误伪装成空回答。

## 面试题

**为什么使用 Message 对象而不是拼接字符串？** 角色、工具调用和多模态内容需要结构化协议，字符串拼接会丢失语义并增加注入风险。

**设置 temperature=0 是否得到确定性结果？** 否。供应商实现、模型版本和并发基础设施仍可能造成差异。

官方资料：[Models](https://docs.langchain.com/oss/python/langchain/models)、[Messages](https://docs.langchain.com/oss/python/langchain/messages)。

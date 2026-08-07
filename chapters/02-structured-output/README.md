# 02 Structured Output

本章让模型返回 `InterviewQuestion`，而不是一段需要自行猜测格式的文本。

```bash
uv run python chapters/02-structured-output/main.py
```

## 数据流

```text
Pydantic Schema -> 模型结构化输出能力 -> 参数解析 -> Pydantic 校验 -> InterviewQuestion
```

字段类型、枚举和长度约束构成应用与模型之间的契约。结构化输出减少解析歧义，但不能证明内容在业务上正确。

## 常见风险

- 兼容 OpenAI 的第三方服务不一定支持原生 JSON Schema。
- Schema 太复杂时，模型可能拒绝或产生校验错误。
- `expected_points` 满足类型约束，不代表评分标准合理。

## 面试题

**Structured Output 和提示模型“返回 JSON”有什么区别？** 前者将 Schema 交给模型接口并在程序侧验证；后者只是自然语言约定。

**为什么还需要业务校验？** 类型系统只能判断形状，不能判断事实、权限和业务规则。

官方资料：[Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)。

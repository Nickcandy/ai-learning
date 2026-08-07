# 12 Eino ADK 与可观测性

本章使用 Eino ReAct Agent 组合 ChatModel、类型安全工具和 Callback。Callback 记录组件名称、类型、耗时和错误，`Context` 负责超时传播。

```bash
go run ./chapters/12-eino-adk-and-observability
go test ./chapters/12-eino-adk-and-observability
```

## 关键边界

- Tool Schema 来自 Go 结构体标签，执行函数仍需业务校验。
- `MaxStep` 防止 ReAct 循环失控。
- Callback 不能修改共享输入输出，否则并发执行时可能产生数据竞争。
- Stream Callback 获得的 Reader 副本必须关闭，否则会泄漏 goroutine。

## 面试题

**ReAct 和 Graph 如何选择？** 开放式工具决策适合 ReAct；明确业务步骤适合 Graph；真实系统经常在 Graph 的局部节点中使用 Agent。

官方资料：[ReAct Agent](https://www.cloudwego.io/docs/eino/core_modules/flow_integration_components/react_agent_manual/)、[Callback](https://www.cloudwego.io/docs/eino/core_modules/chain_and_graph_orchestration/callback_manual/)。

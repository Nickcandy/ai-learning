# 课程总纲

课程围绕同一个业务目标逐步展开：构建一个能基于学习资料出题、追问、评分、保存进度并生成报告的 AI Agent 面试教练。

| 章 | 主题 | 框架 | 本章产物 | 验收重点 |
|---|---|---|---|---|
| 01 | Model 与 Messages | LangChain | 最小多轮对话 | 理解消息角色和模型配置 |
| 02 | Structured Output | LangChain | 类型安全的面试题 | 模型输出可验证、失败可见 |
| 03 | Tools 与 Agent Loop | LangChain | 时间和计算 Agent | 看懂完整工具调用循环 |
| 04 | Streaming 与 Trace | LangChain | 流式事件观察器 | 区分模型、工具和最终输出 |
| 05 | RAG 数据准备 | LangChain | Markdown 切分器 | Chunk 保留来源元数据 |
| 06 | Retrieval 与引用 | LangChain | 带引用的资料问答 | 找不到依据时拒答 |
| 07 | RAG Evaluation | Python | 离线评测器 | 用数据衡量检索质量 |
| 08 | StateGraph 工作流 | LangGraph | 面试状态机 | 区分确定性流程与 Agent 决策 |
| 09 | Memory、HITL、Middleware | LangGraph/LangChain | 可恢复面试流程 | Checkpoint、人工确认和安全边界 |
| 10 | Model、Message、Tool | Eino | Go Agent 基础 | 对照 LangChain 核心抽象 |
| 11 | Eino RAG 与 Graph | Eino | Go 检索工作流 | Component、Lambda、Graph |
| 12 | Eino ADK 与可观测性 | Eino | ReAct 与 Callback | Context、错误和 Trace |
| 13 | AI Agent 面试教练 | LangGraph | 完整 CLI 项目 | 检索、出题、评分、记忆、报告 |

## 为什么这样排序

- RAG 先按确定性 Pipeline 实现，确认检索可靠后再交给 Agent 使用。
- LangGraph 放在 Agent Loop 之后，否则只会记住节点 API，不理解循环本质。
- Eino 放在第二阶段，同一概念只学习一次，再关注 Go 的接口、Context 和错误处理。
- Multi-Agent、MCP、Deep Agents 和 A2UI 暂不进入主线。单 Agent 的评测与恢复稳定后再扩展。

## 每章完成标准

每章必须同时满足：示例可以运行、错误不会被吞掉、README 能解释数据流，并包含面试问题与参考要点。只有检索指标、状态流转和报告聚合等关键确定性逻辑保留少量离线测试。

## 最终面试能力

完成课程后应能解释：

1. Agent 和普通 LLM Workflow 的区别。
2. Tool Calling 的消息协议与失败路径。
3. RAG 的切分、召回、重排、引用和评测。
4. LangGraph/Eino Graph 的状态、持久化与恢复。
5. Context Engineering、Memory、Guardrail 和 HITL 的边界。
6. 如何使用成功率、召回率、延迟和成本评估 Agent。
7. 为什么某些场景不应该使用 Multi-Agent。

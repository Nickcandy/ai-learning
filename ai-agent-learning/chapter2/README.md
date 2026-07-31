# Chapter 2：真实 LLM Agent Loop

这个最小实验对应《深入理解 AI Agent》第二章中的：

- `system`、`user`、`assistant`、`tool` 四种消息角色
- `tools` 工具定义
- `assistant.tool_calls -> 执行工具 -> tool result -> 再次调用 LLM`
- 模型在 `get_current_time` 和 `calculate` 之间选择工具
- 最大循环轮数

## 1. 创建虚拟环境

```bash
cd ai-agent-learning/chapter2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. 配置模型

直接编辑当前目录下的 `.env`：

```dotenv
LLM_API_KEY=你的 API Key
LLM_BASE_URL=
LLM_MODEL=你的模型名称
```

使用 OpenAI 时可以把 `LLM_BASE_URL` 留空。使用其他兼容 OpenAI
Chat Completions API 的服务时，填写对应的 Base URL。

`.env` 已被当前目录的 `.gitignore` 忽略，不会被 Git 跟踪。

## 3. 运行

使用默认问题：

```bash
python agent_loop.py
```

传入自己的问题：

```bash
python agent_loop.py "东京现在几点？"
python agent_loop.py "计算 23 乘以 17"
python agent_loop.py "上海现在几点，再计算 23 乘以 17"
```

程序会打印每轮发送给模型的完整 `messages`、API 耗时、Token Usage、
模型返回、工具参数和工具结果，方便观察上下文如何随 Agent 循环增长。

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from time import perf_counter
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from openai import OpenAI


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取指定 IANA 时区的当前日期和时间。",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA 时区名称，例如 Asia/Shanghai。",
                    }
                },
                "required": ["timezone"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行两个数字之间的加、减、乘、除运算。",
            "parameters": {
                "type": "object",
                "properties": {
                    "left": {
                        "type": "number",
                        "description": "左操作数。",
                    },
                    "operator": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "要执行的运算。",
                    },
                    "right": {
                        "type": "number",
                        "description": "右操作数。",
                    },
                },
                "required": ["left", "operator", "right"],
                "additionalProperties": False,
            },
        },
    },
]


def get_current_time(timezone: str) -> dict[str, str]:
    now = datetime.now(ZoneInfo(timezone))
    return {
        "timezone": timezone,
        "datetime": now.isoformat(timespec="seconds"),
        "day_of_week": now.strftime("%A"),
    }


def calculate(left: float, operator: str, right: float) -> dict[str, object]:
    operations = {
        "add": lambda: left + right,
        "subtract": lambda: left - right,
        "multiply": lambda: left * right,
        "divide": lambda: left / right,
    }

    operation = operations.get(operator)
    if operation is None:
        raise ValueError(f"不支持的运算: {operator}")
    if operator == "divide" and right == 0:
        raise ValueError("除数不能为 0")

    return {
        "left": left,
        "operator": operator,
        "right": right,
        "result": operation(),
    }


def execute_tool(name: str, arguments: str) -> str:
    parsed = json.loads(arguments)

    if name == "get_current_time":
        timezone = parsed.get("timezone")
        if not isinstance(timezone, str) or not timezone:
            raise ValueError("get_current_time.timezone 必须是非空字符串")
        result = get_current_time(timezone)
    elif name == "calculate":
        left = parsed.get("left")
        operator = parsed.get("operator")
        right = parsed.get("right")
        if not isinstance(left, (int, float)):
            raise ValueError("calculate.left 必须是数字")
        if not isinstance(operator, str):
            raise ValueError("calculate.operator 必须是字符串")
        if not isinstance(right, (int, float)):
            raise ValueError("calculate.right 必须是数字")
        result = calculate(left, operator, right)
    else:
        raise ValueError(f"未知工具: {name}")

    return json.dumps(result, ensure_ascii=False)


def load_client() -> tuple[OpenAI, str]:
    load_dotenv(Path(__file__).with_name(".env"))

    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    base_url = os.getenv("LLM_BASE_URL")

    if not api_key:
        raise RuntimeError("请先在 .env 中填写 LLM_API_KEY")
    if not model:
        raise RuntimeError("请先在 .env 中填写 LLM_MODEL")

    client = OpenAI(api_key=api_key, base_url=base_url or None)
    return client, model


def run_agent(question: str, max_rounds: int = 5) -> str:
    client, model = load_client()
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个实用助手。涉及当前时间或算术运算时必须调用对应工具，"
                "不要凭模型知识猜测或自行心算。使用中文简洁回答。"
            ),
        },
        {"role": "user", "content": question},
    ]

    for round_number in range(1, max_rounds + 1):
        print(f"\n--- 第 {round_number} 轮调用 LLM ---")
        print("发送给 LLM 的 messages:")
        print(json.dumps(messages, ensure_ascii=False, indent=2))
        started_at = perf_counter()
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        elapsed_seconds = perf_counter() - started_at
        print(f"本轮 API 耗时: {elapsed_seconds:.3f} 秒")
        if response.usage:
            print("Token Usage:")
            print(response.usage.model_dump_json(indent=2, exclude_none=True))

        assistant_message = response.choices[0].message
        print("LLM 返回:")
        print(assistant_message.model_dump_json(indent=2, exclude_none=True))
        messages.append(assistant_message.model_dump(exclude_none=True))

        if not assistant_message.tool_calls:
            if not assistant_message.content:
                raise RuntimeError("模型既没有返回文本，也没有请求调用工具")
            return assistant_message.content

        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            arguments = tool_call.function.arguments
            print(f"模型请求工具: {name}({arguments})")

            result = execute_tool(name, arguments)
            print(f"工具执行结果: {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    raise RuntimeError(f"Agent 超过最大轮数 {max_rounds}，可能陷入循环")


def main() -> None:
    question = " ".join(sys.argv[1:]) or "现在上海和纽约分别几点？"
    answer = run_agent(question)
    print(f"\n最终回答:\n{answer}")


if __name__ == "__main__":
    main()

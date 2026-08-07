"""Chapter 03: a complete tool-calling agent loop."""

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from importlib.util import module_from_spec, spec_from_file_location
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_current_time(timezone: str) -> dict[str, str]:
    """获取指定 IANA 时区的当前日期和时间。"""
    now = datetime.now(ZoneInfo(timezone))
    return {"timezone": timezone, "datetime": now.isoformat(timespec="seconds")}


@tool
def calculate(left: float, operator: str, right: float) -> float:
    """执行 add、subtract、multiply 或 divide 运算。"""
    if operator == "add":
        return left + right
    if operator == "subtract":
        return left - right
    if operator == "multiply":
        return left * right
    if operator == "divide" and right != 0:
        return left / right
    if operator == "divide":
        raise ValueError("除数不能为 0")
    raise ValueError(f"不支持的运算: {operator}")


def build_agent():
    path = Path(__file__).parents[1] / "01-model-and-messages" / "main.py"
    spec = spec_from_file_location("chapter01", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载第 01 章模型配置")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return create_agent(
        model=module.build_model(),
        tools=[get_current_time, calculate],
        system_prompt="涉及时间或计算时必须使用工具。用中文简洁回答。",
    )


def main() -> None:
    inputs = {"messages": [{"role": "user", "content": "上海现在的小时数乘以 7 是多少？"}]}
    result = build_agent().invoke(inputs)
    for message in result["messages"]:
        print(json.dumps(message.model_dump(exclude_none=True), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()

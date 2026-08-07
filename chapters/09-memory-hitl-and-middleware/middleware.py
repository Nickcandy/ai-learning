"""A middleware that turns tool failures into visible ToolMessages."""

from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage


@wrap_tool_call
def visible_tool_errors(request, handler):
    try:
        return handler(request)
    except Exception as exc:
        return ToolMessage(
            content=f"工具执行失败: {exc}",
            tool_call_id=request.tool_call["id"],
        )

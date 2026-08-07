"""Chapter 04: inspect each node update while an agent runs."""

import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from time import perf_counter


def load_agent():
    path = Path(__file__).parents[1] / "03-tools-and-agent-loop" / "main.py"
    spec = spec_from_file_location("chapter03", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载第 03 章 Agent")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_agent()


def main() -> None:
    started_at = perf_counter()
    inputs = {"messages": [{"role": "user", "content": "计算 23 乘以 17"}]}
    for event in load_agent().stream(inputs, stream_mode="updates", version="v2"):
        if event["type"] != "updates":
            continue
        for node, update in event["data"].items():
            messages = update.get("messages", []) if update else []
            payload = messages[-1].model_dump(exclude_none=True) if messages else update
            print(json.dumps({"node": node, "payload": payload}, ensure_ascii=False, indent=2, default=str))
    print(json.dumps({"elapsed_ms": round((perf_counter() - started_at) * 1000, 2)}))


if __name__ == "__main__":
    main()

"""Chapter 02: validate model output with a schema."""

from enum import StrEnum

from pydantic import BaseModel, Field

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


class Difficulty(StrEnum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"


class InterviewQuestion(BaseModel):
    topic: str = Field(min_length=1)
    difficulty: Difficulty
    question: str = Field(min_length=10)
    expected_points: list[str] = Field(min_length=2, max_length=5)


def load_build_model():
    path = Path(__file__).parents[1] / "01-model-and-messages" / "main.py"
    spec = spec_from_file_location("chapter01", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载第 01 章模型配置")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_model


def main() -> None:
    model = load_build_model()()
    structured_model = model.with_structured_output(InterviewQuestion)
    result = structured_model.invoke("生成一道 senior 难度的 RAG 面试题")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

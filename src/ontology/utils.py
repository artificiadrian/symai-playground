from typing import Literal

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def union_literal(values: list[str]):
    return Literal[*values]  # type: ignore[reportInvalidTypeForm] # this is valid (returns Literal[values[0], values[1], ...] type)

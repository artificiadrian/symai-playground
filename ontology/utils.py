from typing import Any, Union, Literal

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")  # required by OpenAI API


def union(*values: Any):
    return Union[*values]  # type: ignore # this, again, does in fact work


def literal(value: str):
    return Literal[value]  # type: ignore # this, again, does in fact work


def union_literal(*values: str):
    return Literal[*values]  # type: ignore # this, again, does in fact work

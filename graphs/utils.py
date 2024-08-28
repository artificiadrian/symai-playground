from typing import TypeVar, Union

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")  # required by OpenAI API


def union(*values: T) -> Union[T, ...]:
    return Union[*values]

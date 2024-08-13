from typing import TypeVar

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")  # required by OpenAI API


ModelT = TypeVar('ModelT', bound=Model)

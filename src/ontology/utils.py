from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, create_model


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def union_literal(values: list[str]):
    return Literal[*values]  # type: ignore[reportInvalidTypeForm] # this is valid (returns Literal[values[0], values[1], ...] type)


# TODO improve this and ensure there are only scalars, union literals and scalar lists
def Partial(type_: type[StrictModel]) -> type[StrictModel]:
    return create_model(
        f"Partial{type_.__name__}",
        __base__=type_.__base__,  # type: ignore
        __module__=type_.__module__,
        **{k: (Optional[v.annotation], v) for k, v in type_.model_fields.items()},  # type: ignore
    )

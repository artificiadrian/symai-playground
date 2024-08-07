from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid")  # because gpt-4(o)(-mini) requires this to be explicitly set


class ScalarType(str, Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"


class ScalarField(_Model):
    type: Literal["scalar"]
    name: str
    value_type: ScalarType


class ScalarListField(_Model):
    type: Literal["scalar_list"]
    name: str
    element_type: ScalarType


class ReferenceField(_Model):
    type: Literal["ref"]
    name: str
    value_type_name: str


class ReferenceListField(_Model):
    type: Literal["ref_list"]
    name: str
    element_type_name: str


Field = ScalarField | ScalarListField | ReferenceField | ReferenceListField


class Type(_Model):
    name: str
    fields: list[Field]


class TypeSystem(_Model):
    base_type: Type

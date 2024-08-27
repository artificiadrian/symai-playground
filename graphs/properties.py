from enum import StrEnum
from typing import Literal

from pydantic import Field

from graphs.utils import StrictModel


class ValueType(StrEnum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"


PropertyType = Literal["scalar", "list", "enum"]


class PropertyBase(StrictModel):
    type: PropertyType
    name: str = Field(description="Name that uniquely identifies the property (camel Case)")
    description: str
    optional: bool


class EnumProperty(PropertyBase):
    type: Literal["enum"]
    values: list[str]


class ScalarProperty(PropertyBase):
    type: Literal["scalar"]
    value_type: ValueType


class ListProperty(PropertyBase):
    type: Literal["list"]
    element_type: ValueType


Property = ScalarProperty | ListProperty | EnumProperty
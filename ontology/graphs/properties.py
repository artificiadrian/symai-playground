from enum import StrEnum
from typing import Literal, Optional

from pydantic import Field
from pydantic.fields import FieldInfo

from ontology.utils import StrictModel, union_literal


class ValueType(StrEnum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"


class PropertyBase(StrictModel):
    type: Literal[
        "scalar", "list", "enum"
    ]  # ugly hack to make sure type property is first to make OpenAI happy
    name: str = Field(
        description="Name that uniquely identifies the property (camel Case)"
    )
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

_value_type_to_python_type: dict[ValueType, type] = {
    ValueType.STRING: str,
    ValueType.FLOAT: float,
    ValueType.INT: int,
    ValueType.BOOLEAN: bool,
}


def _create_property_field(prop: Property) -> tuple[type, FieldInfo]:
    if isinstance(prop, ScalarProperty):
        py_type = _value_type_to_python_type[prop.value_type]
    elif isinstance(prop, ListProperty):
        py_type = list[_value_type_to_python_type[prop.element_type]]
    elif isinstance(prop, EnumProperty):
        py_type = union_literal(*prop.values)

    if prop.optional:
        py_type = Optional[py_type]

    return py_type, Field(description=prop.description)


def create_property_fields(
    properties: list[Property],
):
    return {prop.name: _create_property_field(prop) for prop in properties}

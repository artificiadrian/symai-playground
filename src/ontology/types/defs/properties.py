from typing import Literal, Optional

from pydantic import Field

from ontology.utils import StrictModel, union_literal

ValueType = Literal["string", "int", "float", "bool"]

_value_type_to_cls = {
    "string": str,
    "int": int,
    "float": float,
    "bool": bool,
}


class PropertyDef(StrictModel):
    name: str = Field(
        ...,
        description="Name of property (snake_case). [Can't be 'id', 'source' or 'target']",
    )
    description: str
    optional: bool


class ScalarPropertyDef(PropertyDef):
    value_type: ValueType


class ListPropertyDef(PropertyDef):
    value_type: ValueType


class EnumPropertyDef(PropertyDef):
    values: list[str] = Field(
        ..., description="List of possible values (all in snake_case)"
    )


class PropertyDefs(StrictModel):
    scalars: list[ScalarPropertyDef]
    lists: list[ListPropertyDef]
    enums: list[EnumPropertyDef]


def _create_property_args(prop: PropertyDef, cls: type):
    if prop.optional:
        cls = Optional[cls]  # type: ignore[reportAssignmentType] # feels like magic, but it works

    return prop.name, Field(cls, description=prop.description)


def _create_scalar_property_args(scalar: ScalarPropertyDef):
    return _create_property_args(scalar, _value_type_to_cls[scalar.value_type])


def _create_list_property_args(list_: ListPropertyDef):
    return _create_property_args(list_, list[_value_type_to_cls[list_.value_type]])


def _create_enum_property_args(enum: EnumPropertyDef):
    return _create_property_args(enum, union_literal(enum.values))


def create_property_kwargs(defs: PropertyDefs):
    """Create a dictionary of properties that can be passed to Pydantic's `create_model` (`**props`)"""

    scalars = [_create_scalar_property_args(scalar) for scalar in defs.scalars]
    lists = [_create_list_property_args(list_) for list_ in defs.lists]
    enums = [_create_enum_property_args(enum) for enum in defs.enums]

    # TODO what I don't like about this non-anyOf approach is that the order of the properties is garbage, but tbf it's a dict anyways? check this!

    return {k: v for k, v in scalars + lists + enums}

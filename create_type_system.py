from enum import Enum
from typing import Literal

import pydantic
from symai.components import FunctionWithUsage

from utils import Model


class ScalarType(str, Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"


class ScalarField(Model):
    type: Literal["scalar"]
    name: str
    value_type: ScalarType


class ScalarListField(Model):
    type: Literal["scalar_list"]
    name: str
    element_type: ScalarType


class ReferenceField(Model):
    type: Literal["ref"]
    name: str
    value_type_name: str


class ReferenceListField(Model):
    type: Literal["ref_list"]
    name: str
    element_type_name: str


Field = ScalarField | ScalarListField | ReferenceField | ReferenceListField


class Type(Model):
    name: str
    level: int = pydantic.Field(
        description="Level of the type in the hierarchy. The root type should have level 0, its children level 1, "
                    "and so on.")
    fields: list[Field]


class TypeSystem(Model):
    types: list[Type]


create_prompt = (
    "Create a type system to extract structured information from the given sample text by defining a JSON object. The "
    "system must adhere to the following rules: \n"
    "   1) only one type (root) can exist at level 0\n"
    "   2) types at higher levels cannot reference types at lower levels.\n"
    "Ensure that the type system aligns with the overall goal of clearly structuring information for effective "
    "extraction.")


class CreateTypeSystem(FunctionWithUsage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         static_context=create_prompt,
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "type_system",
                             "schema": TypeSystem.model_json_schema()
                         }})

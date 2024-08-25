from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid")  # required by OpenAI API


class ValueType(StrEnum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"


# duplicate code in properties is for now (unfortunately) intentional as a common base class resulted in OpenAI API 
# errors regarding anyOf implementation and ordering of variables

class _Property(_Model):
    type: Literal["scalar", "list", "enum"]
    name: str = Field(description="Name that uniquely identifies the property (camel Case)")
    description: str
    optional: bool


class EnumProperty(_Property):
    type: Literal["enum"]
    name: str
    values: list[str]


class ScalarProperty(_Property):
    type: Literal["scalar"]
    name: str
    value_type: ValueType


class ListProperty(_Property):
    type: Literal["list"]
    name: str
    element_type: ValueType


Property = ScalarProperty | ListProperty | EnumProperty


class NodeDefinition(_Model):
    name: str = Field(description="Name that uniquely identifies the node type (Pascal case)")
    description: str
    properties: list[Property]


class EdgeDefinition(_Model):
    name: str = Field(description="Name that uniquely identifies the edge type (Pascal case)")
    description: str
    properties: list[Property]

    a: str = Field(description="Name of the node type at one end of the edge (Pascal case)")
    b: str = Field(description="Name of the node type at the other end of the edge (Pascal case)")


def _ensure_names_are_unique(items: list, error: str):
    names = set()
    for item in items:
        if item.name in names:
            raise ValueError(error.format(name=item.name))

        names.add(item.name)


# TODO validate name lengths

class GraphDefinition(_Model):
    nodes: list[NodeDefinition]
    edges: list[EdgeDefinition]

    @model_validator(mode='after')
    def validate_edges(self):
        _ensure_names_are_unique(self.edges, "Edge name '{name}' is not unique")

        node_names = {node.name for node in self.nodes}
        for edge in self.edges:
            if edge.a not in node_names:
                raise ValueError(f"Edge 'a' value '{edge.a}' does not exist in nodes for edge '{edge.name}'")
            if edge.b not in node_names:
                raise ValueError(f"Edge 'b' value '{edge.b}' does not exist in nodes for edge '{edge.name}'")

            _ensure_names_are_unique(edge.properties, f"Property name '{{name}}' of edge '{edge.name}' is not unique")

        return self

    @model_validator(mode='after')
    def validate_nodes(self):
        _ensure_names_are_unique(self.nodes, "Node name '{name}' is not unique")
        return self

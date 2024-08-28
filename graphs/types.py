from typing import Literal, Optional

from pydantic import BaseModel, create_model

from create_type_system import Field
from graphs.commands.create_types import NodeTypeDefinition, EdgeTypeDefinition
from graphs.data import Node, Edge
from graphs.properties import EnumProperty, Property, ScalarProperty, ListProperty, ValueType

_value_type_to_python_type: dict[ValueType, type] = {
    ValueType.STRING: str,
    ValueType.FLOAT: float,
    ValueType.INT: int,
    ValueType.BOOLEAN: bool,
}


def _create_enum_as_literal_union(prop: EnumProperty):
    """Dynamically create a union of Literal types for an enum property"""
    return Literal[*prop.values]


def _create_property_field(prop: Property):
    if isinstance(prop, ScalarProperty):
        py_type = _value_type_to_python_type[prop.value_type]
    elif isinstance(prop, ListProperty):
        py_type = list[_value_type_to_python_type[prop.element_type]]
    elif isinstance(prop, EnumProperty):
        py_type = _create_enum_as_literal_union(prop)
    else:
        raise ValueError(f"Unknown property type: {prop}")

    if prop.optional:
        py_type = Optional[py_type]

    return py_type, Field(description=prop.description)


def _create_property_fields(properties: list[Property]):
    props = {p.name: _create_property_field(p) for p in properties}
    props["id"] = (str, Field(description="Globally unique identifier (camelCase)!"))
    props["display_name"] = str, Field(...,
                                       description="Display name. For nodes, this is the name of the node. For edges, "
                                                   "describe what the edge is about, but do not mention the nodes.")
    return props


def _create_type(definition, base: type[BaseModel], **props):
    return create_model(
        definition.name,
        __base__=base,
        **_create_property_fields(definition.properties),
        **props,
    )


def create_node_type(node_type: NodeTypeDefinition):
    return _create_type(node_type, Node)


def create_edge_type(edge_type: EdgeTypeDefinition):
    return _create_type(edge_type, Edge,
                        a=(str, Field(
                            description=f"Unique identifier of the {edge_type.source} node at one end of the "
                                        f"edge (camel Case)")),
                        b=(str, Field(
                            description=f"Unique identifier of the {edge_type.target} node at the other end of "
                                        f"the edge (camel "
                                        f"Case)")),
                        )

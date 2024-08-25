import re
from enum import StrEnum
from typing import Optional

from pydantic import Field, create_model, BaseModel

from graphs.models import (
    EnumProperty,
    GraphDefinition,
    ListProperty,
    Property,
    ScalarProperty,
    ValueType, EdgeDefinition,
)

_value_type_to_python_type: dict[ValueType, type] = {
    ValueType.STRING: str,
    ValueType.FLOAT: float,
    ValueType.INT: int,
    ValueType.BOOLEAN: bool,
}

_pascal_to_snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def _create_str_enum(prop: EnumProperty):
    return StrEnum(prop.name, {v: v for v in prop.values})


def _create_property_field(prop: Property):
    if isinstance(prop, ScalarProperty):
        py_type = _value_type_to_python_type[prop.value_type]
    elif isinstance(prop, ListProperty):
        py_type = list[_value_type_to_python_type[prop.element_type]]
    elif isinstance(prop, EnumProperty):
        py_type = _create_str_enum(prop)

    if prop.optional:
        py_type = Optional[py_type]

    return py_type, Field(description=prop.description)


def _create_property_fields(properties: list[Property]):
    props = {p.name: _create_property_field(p) for p in properties}
    props["id"] = (str, Field(description="Unique identifier of the node (camel Case)"))
    return props


def _create_type(definition, base: type[BaseModel], **props):
    return create_model(
        definition.name,
        __base__=base,
        __module__="custom_graph",
        **_create_property_fields(definition.properties),
        **props,
    )


def _create_edge_type(edge: EdgeDefinition, base: type[BaseModel]):
    return _create_type(edge, base,
                        a=(str, Field(
                            description=f"Unique identifier of the {edge.a} node at one end of the edge (camel Case)")),
                        b=(str, Field(
                            description=f"Unique identifier of the {edge.b} node at the other end of the edge (camel "
                                        f"Case)")),
                        )


def _types_to_list_fields(types: list[type[BaseModel]]):
    return {_pascal_to_snake_case_pattern.sub('_', t.__name__).lower(): (list[t], Field(default_factory=lambda: [])) for
            t in types}


def create_pydantic_types(graph: GraphDefinition):
    # todo allow custom module!
    node_base_type = create_model("Node", __module__="custom_graph")
    edge_base_type = create_model("Edge", __module__="custom_graph")

    node_types = [_create_type(node, node_base_type) for node in graph.nodes]
    edge_types = [_create_edge_type(edge, edge_base_type) for edge in graph.edges]

    graph_types_type = create_model(
        "GraphTypes",
        node_types=(dict[str, type[node_base_type]], Field(description="Nodes")),
        edge_types=(dict[str, type[edge_base_type]], Field(description="Edges")),
    )

    graph_type = create_model(
        "Graph",
        **_types_to_list_fields(node_types + edge_types)
    )

    return graph_types_type(node_types={t.__name__: t for t in node_types},
                            edge_types={e.__name__: e for e in edge_types}), graph_type()

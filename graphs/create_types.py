import re
from typing import Optional, cast, Literal

from pydantic import Field, create_model, BaseModel

from graphs.models import (
    EnumProperty,
    GraphDefinition,
    ListProperty,
    Property,
    ScalarProperty,
    ValueType, EdgeDefinition, NodeDefinition, StrictModel,
)

_value_type_to_python_type: dict[ValueType, type] = {
    ValueType.STRING: str,
    ValueType.FLOAT: float,
    ValueType.INT: int,
    ValueType.BOOLEAN: bool,
}

_pascal_to_snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def _pascal_to_snake_case(pascal: str):
    return _pascal_to_snake_case_pattern.sub('_', pascal).lower()


class Node(StrictModel):
    pass


class Edge(StrictModel):
    pass


class BaseGraph(StrictModel):
    pass


def _create_enum_as_literal_union(prop: EnumProperty):
    """Dynamically create a union of Literal types for an enum property"""
    return Literal[tuple(prop.values)]


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
    props["id"] = (str, Field(description="Globally unique identifier of the node (camel Case)!"))
    return props


def _create_type(definition, base: type[BaseModel], **props):
    return create_model(
        definition.name,
        __base__=base,
        __module__="custom_graph",
        **_create_property_fields(definition.properties),
        **props,
    )


def _create_node_type(node: NodeDefinition):
    return cast(type[Node], _create_type(node, Node))


def _create_edge_type(edge: EdgeDefinition):
    return cast(type[Edge], _create_type(edge, Edge,
                                         a=(str, Field(
                                             description=f"Unique identifier of the {edge.a} node at one end of the "
                                                         f"edge (camel Case)")),
                                         b=(str, Field(
                                             description=f"Unique identifier of the {edge.b} node at the other end of "
                                                         f"the edge (camel "
                                                         f"Case)")),
                                         ))


def _types_to_list_fields(types: list[type[Node] | type[Edge]]):
    return {_pascal_to_snake_case(t.__name__): (list[t], ...) for
            t in types}


def create_graph_type(graph: GraphDefinition, module: str = "custom_graph"):
    # TODO check if name collisions in modules are a problem!

    node_types = [_create_node_type(node) for node in graph.nodes]
    edge_types = [_create_edge_type(edge) for edge in graph.edges]

    fields = _types_to_list_fields(node_types + edge_types)

    graph_type = create_model(
        "Graph",
        __module__=module,
        __base__=BaseGraph,
        **fields
    )

    def __init__(self, **kwargs):
        """Creates an empty instance of the generated graph type with empty lists by default"""
        super(graph_type, self).__init__(**{k: kwargs.get(k, []) for k in fields.keys()})

    # set custom __init__ function s.t. calling `graph_type()` creates a graph with empty lists
    graph_type.__init__ = __init__

    return graph_type

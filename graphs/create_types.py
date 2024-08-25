from enum import StrEnum

from pydantic import create_model, Field

from graphs.models import GraphDefinition, Property, ValueType, EnumProperty, ScalarProperty, \
    ListProperty

_value_type_to_python_type = {
    ValueType.STRING: str,
    ValueType.FLOAT: float,
    ValueType.INT: int,
    ValueType.BOOLEAN: bool
}


def _create_str_enum(prop: EnumProperty):
    return StrEnum(prop.name, {v: v for v in prop.values})


def _create_property_field(prop: Property):
    if isinstance(prop, ScalarProperty):
        py_type = _value_type_to_python_type[prop.value_type]
    elif isinstance(prop, ListProperty):
        py_type = list[_value_type_to_python_type[prop.element_type]]
    elif isinstance(prop, EnumProperty):
        py_type = _create_str_enum(prop)
    else:
        raise ValueError(f"Unknown property type {prop.type}")

    if prop.optional:
        py_type = py_type | None

    return py_type, Field(description=prop.description)


def _create_property_fields(properties: list[Property]):
    return {p.name: _create_property_field(p) for p in properties}


def _create_type(definition):
    return create_model(definition.name, id=(str, Field(description="A unique identifier for the object (camel Case)")),
                        **_create_property_fields(definition.properties),
                        __module__="custom_graph")


def create_pydantic_types(graph: GraphDefinition):
    node_types = [_create_type(node) for node in graph.nodes]
    edge_types = [_create_type(edge) for edge in graph.edges]

    return create_model("Graph", nodes=(node_types, Field(description="Nodes")),
                        edges=(edge_types, Field(description="Edges")))

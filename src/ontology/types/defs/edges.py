from pydantic import Field, create_model

from ontology.types.defs.base import TypeDef
from ontology.types.defs.properties import create_property_kwargs
from ontology.types.edges import Edge
from ontology.types.vertices import Vertex
from ontology.utils import union_literal


class EdgeTypeDef(TypeDef):
    pass


def create_edge_type_def(vertex_types: list[type[Vertex]]) -> type[EdgeTypeDef]:
    """Creates a new Edge type definition that enforces existing source and target Vertex type names"""

    vertex_type_names = [
        vt.__class__.__name__ for vt in vertex_types
    ]  # TODO change this to use the name attribute

    name_union_literal = union_literal(vertex_type_names)

    return create_model(
        "StrictEdgeTypeDef",
        __base__=EdgeTypeDef,
        source_vertex_type=(
            name_union_literal,
            Field(..., description="Name of existing source Vertex type (PascalCase)"),
        ),
        target_vertex_type=(
            name_union_literal,
            Field(..., description="Name of existing target Vertex type (PascalCase)"),
        ),
    )


def create_edge_type(etd: EdgeTypeDef):
    # need to get `src_vt` and `tgt_vt` manually as they are dynamically created in `create_edge_type_def `
    src_vt: str = getattr(etd, "source_vertex_type")
    tgt_vt: str = getattr(etd, "target_vertex_type")

    props = create_property_kwargs(etd.props)

    # TODO contextualize these errors, add custom exception types

    if "source" in props:
        raise ValueError("Cannot define a property named 'source'")

    if "target" in props:
        raise ValueError("Cannot define a property named 'target'")

    cls = create_model(
        etd.name,
        __base__=Edge,
        source=Field(..., description=f"Id of source {src_vt} Vertex"),
        target=Field(..., description=f"Id of target {tgt_vt} Vertex"),
        **props,
    )

    cls.__doc__ = etd.description

    return cls

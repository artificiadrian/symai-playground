from types import UnionType
from typing import cast

from ontology.graphs.commands.add import (
    create_add_edges_command,
    create_add_vertices_command,
)
from ontology.graphs.commands.create_types import (
    CreateEdgeTypesCommand,
    CreateVertexTypesCommand,
)
from ontology.graphs.commands.delete import DeleteEdgesCommand, DeleteVerticesCommand
from ontology.graphs.edges import Edge
from ontology.graphs.vertices import Vertex


def create_any_command_type(
    vertex_types: list[type[Vertex]], edge_types: list[type[Edge]]
):
    union = (
        CreateVertexTypesCommand
        | DeleteVerticesCommand
        | CreateEdgeTypesCommand
        | DeleteEdgesCommand
    )

    if len(vertex_types) > 0:
        union |= create_add_vertices_command(vertex_types)

    if len(edge_types) > 0:
        union |= create_add_edges_command(edge_types)

    return cast(UnionType, union)

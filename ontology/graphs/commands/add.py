from typing import Literal

from pydantic import create_model

from ontology.graphs.commands.base import BaseCommand
from ontology.graphs.edges import Edge
from ontology.graphs.vertices import Vertex
from ontology.utils import union


class BaseAddVerticesCommand(BaseCommand):
    name: Literal["AddVertices"]


class BaseAddEdgesCommand(BaseCommand):
    name: Literal["AddEdges"]


def create_add_vertices_command(vertex_types: list[type[Vertex]]):
    return create_model(
        "AddVerticesCommand",
        __base__=BaseAddVerticesCommand,
        vertices=(list[union(vertex_types)], ...),
    )


def create_add_edges_command(edge_types: list[type[Edge]]):
    return create_model(
        "AddEdgesCommand",
        __base__=BaseAddEdgesCommand,
        edges=(list[union(edge_types)], ...),
    )

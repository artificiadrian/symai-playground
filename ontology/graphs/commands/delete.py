from typing import Literal

from ontology.graphs.commands.base import BaseCommand


class DeleteVerticesCommand(BaseCommand):
    name: Literal["DeleteVertices"]

    vertex_ids: list[str]


class DeleteEdgesCommand(BaseCommand):
    name: Literal["DeleteEdges"]

    edge_ids: list[str]

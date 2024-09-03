from typing import Literal

from ontology.graphs.commands.base import BaseCommand
from ontology.graphs.edges import EdgeTypeDef
from ontology.graphs.vertices import VertexTypeDef


class CreateVertexTypesCommand(BaseCommand):
    name: Literal["CreateVertexTypes"]

    new_types: list[VertexTypeDef]


class CreateEdgeTypesCommand(BaseCommand):
    name: Literal["CreateEdgeTypes"]

    new_types: list[EdgeTypeDef]

from typing import Literal, ClassVar

from graphs.commands.types.base import BaseCommand, CommandInfo
from graphs.properties import Property
from graphs.utils import StrictModel


class EdgeType(StrictModel):
    name: str
    description: str
    properties: list[Property]


class NodeType(StrictModel):
    name: str
    description: str
    properties: list[Property]


class CreateEdgeTypesCommand(BaseCommand):
    cmd: Literal["create_edge_types"]
    info: ClassVar[CommandInfo] = CommandInfo(description="Create new edge types")

    new_types: list[EdgeType]


class CreateNodeTypesCommand(BaseCommand):
    cmd: Literal["create_node_types"]
    info: ClassVar[CommandInfo] = CommandInfo(description="Create new node types")

    new_types: list[NodeType]

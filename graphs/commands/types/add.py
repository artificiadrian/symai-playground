from typing import Literal, ClassVar

from graphs.commands.types.base import BaseCommand, CommandInfo
from graphs.graph.edge import Edge
from graphs.graph.node import Node


class AddNodesCommand(BaseCommand):
    cmd: Literal["add_nodes"]
    info: ClassVar[CommandInfo] = CommandInfo(description="Add new nodes to the graph")

    nodes: list[Node]


class AddEdgesCommand(BaseCommand):
    cmd: Literal["add_edges"]
    info: ClassVar[CommandInfo] = CommandInfo(description="Add new edges to the graph")

    edges: list[Edge]

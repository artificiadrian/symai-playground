from typing import Literal, ClassVar

from graphs.commands.types.base import BaseCommand, CommandInfo


class DeleteEdgesCommand(BaseCommand):
    cmd: Literal["delete_edges"]
    info: ClassVar[CommandInfo] = CommandInfo(description="Delete edges from the graph")

    edge_ids: list[str]


class DeleteNodesCommand(BaseCommand):
    cmd: Literal["delete_nodes"]
    info: ClassVar[CommandInfo] = CommandInfo(
        description="Delete nodes from the graph (make sure to delete corresponding edges first!)")

    node_ids: list[str]

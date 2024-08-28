from typing import Literal

from graphs.commands.base import BaseCommand, CommandName


class DeleteEdgesCommand(BaseCommand):
    cmd: Literal[CommandName.delete_edges]

    edge_ids: list[str]


class DeleteNodesCommand(BaseCommand):
    cmd: Literal[CommandName.delete_nodes]

    node_ids: list[str]

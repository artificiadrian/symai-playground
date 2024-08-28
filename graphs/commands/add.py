from collections.abc import Iterable

from graphs.commands.base import create_command_type, CommandName
from graphs.data import Node, Edge
from graphs.utils import union


def create_add_nodes_command(node_types: Iterable[type[Node]]):
    return create_command_type("AddNodesCommand", CommandName.add_nodes, "Add new nodes to the graph",
                               nodes=(list[union(node_types)],))


def create_add_edges_command(edge_types: Iterable[type[Edge]]):
    return create_command_type("AddEdgesCommand", CommandName.add_edges, "Add new edges to the graph",
                               edges=(list[union(edge_types)],))

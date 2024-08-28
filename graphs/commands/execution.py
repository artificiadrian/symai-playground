from pydantic import create_model

from graphs.commands.add import create_add_nodes_command, create_add_edges_command
from graphs.commands.create_types import CreateNodeTypesCommand, CreateEdgeTypesCommand
from graphs.commands.delete import DeleteNodesCommand, DeleteEdgesCommand
from graphs.graph import Graph
from graphs.utils import StrictModel

_StaticCommands = CreateNodeTypesCommand | CreateEdgeTypesCommand | DeleteNodesCommand | DeleteEdgesCommand


def create_execute_commands_type(graph: Graph):
    AnyCommand = _StaticCommands | create_add_nodes_command(graph.node_types.values()) | create_add_edges_command(
        graph.edge_types.values())

    return create_model("ExecuteCommands", __base__=StrictModel, commands=(list[AnyCommand],))

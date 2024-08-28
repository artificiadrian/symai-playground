from graphs.commands.base import BaseCommand
from graphs.commands.create_types import CreateNodeTypesCommand, CreateEdgeTypesCommand
from graphs.commands.execution import create_execute_commands_type
from graphs.graph import Graph
from graphs.types import create_node_type, create_edge_type


class GraphCommander:
    __slots__ = ("_graph", "_execute_commands_type")

    def __init__(self):
        self._graph = Graph()
        self._execute_commands_type = create_execute_commands_type(self._graph)

    @property
    def execute_commands_type(self):
        return self._execute_commands_type

    def _update_exec_type(self):
        self._execute_commands_type = create_execute_commands_type(self._graph)

    def _exec_create_node_types_command(self, cmd: CreateNodeTypesCommand):
        for node_type in cmd.new_types:
            self._graph.add_node_type(create_node_type(node_type))

    def _exec_create_edge_types_command(self, cmd: CreateEdgeTypesCommand):
        for edge_type in cmd.new_types:
            self._graph.add_edge_type(create_edge_type(edge_type))

    def _execute_command(self, command: BaseCommand):
        match command:
            case CreateNodeTypesCommand() as cntc:
                self._exec_create_node_types_command(cntc)
            case CreateEdgeTypesCommand() as cetc:
                self._exec_create_edge_types_command(cetc)
            case _:
                raise ValueError(f"Unsupported command: {command.cmd}")

    def execute_commands(self, *commands: BaseCommand):
        for command in commands:
            self._execute_command(command)
            
        self._update_exec_type()

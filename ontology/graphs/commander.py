from ontology.graphs.commands.add import BaseAddEdgesCommand, BaseAddVerticesCommand
from ontology.graphs.commands.base import BaseCommand
from ontology.graphs.commands.create_types import (
    CreateEdgeTypesCommand,
    CreateVertexTypesCommand,
)
from ontology.graphs.commands.delete import DeleteEdgesCommand, DeleteVerticesCommand
from ontology.graphs.commands.union import create_any_command_type
from ontology.graphs.edges import create_edge_type
from ontology.graphs.graph import Graph
from ontology.graphs.vertices import create_vertex_type


class GraphCommander:
    __slots__ = ("_graph", "_any_command_type")

    def __init__(self):
        self._graph = Graph()
        self._any_command_type = create_any_command_type(
            list(self._graph.vertex_types.values()),
            list(self._graph.edge_types.values()),
        )

    @property
    def graph(self):
        return self._graph

    @property
    def any_command_type(self):
        return self._any_command_type

    def _update_any_command_type(self):
        self._any_command_type = create_any_command_type(
            list(self._graph.vertex_types.values()),
            list(self._graph.edge_types.values()),
        )

    def execute(self, cmd: BaseCommand):
        print("Executing", cmd.__class__.__name__, cmd.model_dump_json(indent=4))
        if isinstance(cmd, CreateVertexTypesCommand):
            for vt in cmd.new_types:
                print(vt)
                self._graph.add_vertex_type(create_vertex_type(vt))
            self._update_any_command_type()

        elif isinstance(cmd, CreateEdgeTypesCommand):
            for et in cmd.new_types:
                self._graph.add_edge_type(create_edge_type(et))
            self._update_any_command_type()

        elif isinstance(cmd, DeleteVerticesCommand):
            self._graph.data.vertices = [
                v for v in self._graph.data.vertices if v.id not in cmd.vertex_ids
            ]

        elif isinstance(cmd, DeleteEdgesCommand):
            self._graph.data.edges = [
                e for e in self._graph.data.edges if e.id not in cmd.edge_ids
            ]

        elif isinstance(cmd, BaseAddVerticesCommand):
            self._graph.data.vertices.extend(getattr(cmd, "vertices"))

        elif isinstance(cmd, BaseAddEdgesCommand):
            self._graph.data.edges.extend(getattr(cmd, "edges"))

        else:
            raise ValueError(f"Unknown command type: {cmd}")

from collections.abc import Mapping

from ontology.graphs.data import GraphData
from ontology.graphs.edges import Edge
from ontology.graphs.vertices import Vertex


class Graph:
    __slots__ = ("_vertex_types", "_edge_types", "_data")

    def __init__(self):
        self._vertex_types = dict[str, type[Vertex]]()  # TODO enforce read-only?
        self._edge_types = dict[str, type[Edge]]()

        self._data = GraphData(vertices=[], edges=[])

    @property
    def data(self):
        return self._data

    @property
    def vertex_types(self) -> Mapping[str, type[Vertex]]:
        return self._vertex_types

    @property
    def edge_types(self) -> Mapping[str, type[Edge]]:
        return self._edge_types

    def add_vertex_type(self, vt: type[Vertex]):
        name = vt.__name__  # TODO set name manually?

        if name in self._vertex_types:
            raise ValueError(f"Vertex type {name} already exists")

        self._vertex_types[name] = vt

    def add_edge_type(self, et: type[Edge]):
        name = et.__name__

        if name in self._edge_types:
            raise ValueError(f"Edge type {name} already exists")

        self._edge_types[name] = et

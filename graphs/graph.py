from graphs.data import GraphData, Node, Edge


class Graph:
    def __init__(self):
        self._node_types = dict[str, type[Node]]()
        self._edge_types = dict[str, type[Edge]]()
        self._data = GraphData()

    @property
    def node_types(self):
        return dict(self._node_types)

    @property
    def edge_types(self):
        return dict(self._edge_types)

    def add_node_type(self, node_type: type[Node]):
        name = node_type.__name__

        if name in self._node_types:
            raise ValueError(f"Node type {name} already exists")

        self._node_types[name] = node_type

    def add_edge_type(self, edge_type: type[Edge]):
        name = edge_type.__name__

        if name in self._edge_types:
            raise ValueError(f"Edge type {name} already exists")

        self._edge_types[name] = edge_type

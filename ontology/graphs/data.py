from ontology.graphs.edges import Edge
from ontology.graphs.vertices import Vertex
from ontology.utils import StrictModel


class GraphData(StrictModel):
    vertices: list[Vertex]
    edges: list[Edge]

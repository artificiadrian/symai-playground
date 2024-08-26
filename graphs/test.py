from pathlib import Path

from symai import Symbol

from graphs.create_types import BaseGraph
from graphs.expressions.create_graph import CreateGraph
from graphs.expressions.fill_graph import FillGraph
import networkx as nx
from pyvis.network import Network

g = CreateGraph()

sym = g(Symbol(
    "I want to build an ontology for a fiction story. Characters as nodes and relationships as edges. Add properties "
    "to them. No other node or edge types."))
graph_type: type[BaseGraph] = sym.value

graph = graph_type()
print("Graph:", graph)

print("Schema:", graph.model_json_schema())

paper_text = Symbol(Path("examples/romeo_and_juliet.txt").read_text(encoding="utf-8"))

fg = FillGraph(graph)
print("Filling...\n")

sym = fg(paper_text)
graph = sym.value
print(sym, graph)

with open("examples/graph.json", "w") as f:
    f.write(graph.model_dump_json(indent=4))

G = nx.Graph()
for node in graph.get_nodes():
    G.add_node(node.uid, label=node.get_display_name())

for edge in graph.get_edges():
    G.add_edge(edge.a, edge.b, label=edge.get_display_name())

network = Network()
network.from_nx(G)
network.save_graph("examples/graph.html")
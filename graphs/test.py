from symai import Symbol

from graphs.create_types import BaseGraph
from graphs.expressions.create_graph import CreateGraph
from graphs.expressions.fill_graph import FillGraph

g = CreateGraph()

sym = g(Symbol("I want to build a character-relationship graph from a fiction book. Focus on characters and their relationships."))
graph_type: type[BaseGraph] = sym.value

graph = graph_type()
print("Graph:", graph)

print("Schema:", graph.model_json_schema())

with open("examples/romeo_and_juliet.txt", "r", encoding="utf-8") as f:
    text = Symbol(f.read()[:20000])

fg = FillGraph(graph)
print("Filling...\n")

sym = fg(text)
print(sym.value.model_dump_json(indent=4))

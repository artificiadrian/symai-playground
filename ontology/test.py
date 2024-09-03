from pathlib import Path

from ontology.expressions.work_on_graph import WorkOnGraph
from ontology.graphs.commander import GraphCommander

text = Path("samples/white_nights.txt").read_text(encoding="utf-8")
text = text[10000:50000]

work = WorkOnGraph(task="I want a relationship graph", commander=GraphCommander())


x = work.forward(text)

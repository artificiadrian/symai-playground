from pathlib import Path

from symai import Symbol
from symai.components import Function

from graphs.create_types import BaseGraph

_fill_prompt = Path("prompts/fill_graph_prompt.txt").read_text()


class FillGraph(Function):
    def __init__(self, graph: BaseGraph, extra_info: str = "", prompt: str = _fill_prompt, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         static_context=prompt.format(graph=graph.model_dump_json(), extra_info=extra_info),
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "graph_schema",
                             "schema": graph.model_json_schema()
                         }})
        self._graph = graph

    def forward(self, *args, **kwargs):
        x = super().forward(*args, **kwargs)
        return Symbol(self._graph.model_validate_json(x.value))

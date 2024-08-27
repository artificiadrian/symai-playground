from pathlib import Path

from symai import Symbol
from symai.components import Function

from oldgraphs.create_types import create_graph_type
from oldgraphs.models import GraphDefinition

_create_prompt = Path("prompts/create_graph_prompt.txt").read_text()


class CreateGraph(Function):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         static_context=_create_prompt,
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "graph_definition",
                             "schema": GraphDefinition.model_json_schema()
                         }})

    def forward(self, *args, **kwargs):
        x = super().forward(*args, **kwargs)
        definition = GraphDefinition.model_validate_json(x.value)
        return Symbol(create_graph_type(definition))

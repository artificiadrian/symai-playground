from pathlib import Path

from symai import Symbol
from symai.components import FunctionWithUsage

from graphs.create_types import create_pydantic_types
from graphs.models import GraphDefinition

_create_prompt = Path("prompts/create_graph_prompt.txt").read_text()


class CreateGraph(FunctionWithUsage):
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
        print(x[0])
        return Symbol(GraphDefinition.model_validate_json(x[0])), x[1]


g = CreateGraph()

sym = g(Symbol("I want to build the ultimate knowledge graph from a book about the history of the world."))
graph: GraphDefinition = sym[0].value

print(create_pydantic_types(graph))

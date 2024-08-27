from pathlib import Path

from pydantic import ValidationError
from symai import Symbol
from symai.components import Function

from oldgraphs.create_types import BaseGraph

_fill_prompt = Path("prompts/fill_graph_prompt.txt").read_text()
_fix_prompt = Path("prompts/fix_graph_prompt.txt").read_text()


# TODO include information on how to fix our custom errors s.t. the model has it easier!

def _format_error(error: ValidationError):
    return f"<error>{error.json()}</error>"


class FixGraph(Function):
    def __init__(self, graph: BaseGraph, error: ValidationError, extra_info: str = "",
                 fix_prompt: str = _fix_prompt, max_retries: int = 5,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs,
                         static_context=fix_prompt.format(graph=graph.model_dump_json(), extra_info=extra_info),
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "graph_schema",
                             "schema": graph.model_json_schema()
                         }})

        self._graph = graph
        self._initial_error = error
        self._max_retries = max_retries

    def forward(self, *args, **kwargs):
        print("Fixing graph")
        error = self._initial_error
        for i in range(self._max_retries):
            print(f"[{i + 1}/{self._max_retries}] Trying to fix graph because of", error.json())
            self.adapt(_format_error(error))
            x = super().forward(*args, **kwargs)
            try:
                model = self._graph.model_validate_json(x.value)
                return Symbol(model)
            except ValidationError as e:
                error = e

        raise Exception("Could not fix graph") from error


class FillGraph(Function):
    def __init__(self, graph: BaseGraph, extra_info: str = "", fill_prompt: str = _fill_prompt,
                 *args, **kwargs):
        super().__init__(*args, **kwargs,
                         static_context=fill_prompt.format(graph=graph.model_dump_json(), extra_info=extra_info),
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "graph_schema",
                             "schema": graph.model_json_schema()
                         }})

        self._graph = graph

    def forward(self, *args, **kwargs):
        x = super().forward(*args, **kwargs)
        try:
            print(x.value)
            model = self._graph.model_validate_json(x.value)
            print("model is valid", model)
            return Symbol(model)
        except ValidationError as e:
            print("error in model, fixing", e)
            fixer = FixGraph(self._graph, e)
            return fixer(x)

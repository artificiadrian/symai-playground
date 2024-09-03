from pathlib import Path
from types import UnionType

from pydantic import create_model
from symai import Expression, Function, Symbol

from ontology.graphs.commander import GraphCommander
from ontology.utils import StrictModel

_command_prompt = Path("prompts/command_graph_prompt.txt").read_text()


# TODO maybe allow model to change or add new tasks?
def create_execute_commands_model(any_command_type: UnionType):
    cls = create_model(
        "ExecuteCommands",
        __base__=StrictModel,
        commands=(list[any_command_type], ...),
    )
    cls.__doc__ = (
        "Execute a list of commands to transform a graph (make sure they are in order!)"
    )

    return cls


class CommandGraph(Function):
    def __init__(self, task: str, commander: GraphCommander, *args, **kwargs):
        self._exec_model = create_execute_commands_model(commander.any_command_type)
        super().__init__(
            *args,
            **kwargs,
            static_context=_command_prompt.format(
                task=task, graph=commander.graph.data.model_dump_json()
            ),
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "strict": True,
                    "name": "commands",
                    "schema": self._exec_model.model_json_schema(),
                },
            },
        )

    def forward(self, *args, **kwargs):
        x = super().forward(*args, **kwargs)
        exec = self._exec_model.model_validate_json(x.value)
        return Symbol(exec)


class WorkOnGraph(Expression):
    def __init__(
        self,
        task: str,
        commander: GraphCommander,
        iterations: int = 10,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._task = task
        self._iterations = iterations
        self._commander = commander

    def forward(self, *args, **kwargs):
        task = self._task
        for i in range(self._iterations):
            func = CommandGraph(task, self._commander, *args, **kwargs)
            graph_symbol: Symbol = func.forward(*args, **kwargs)
            commands = graph_symbol.value

            for cmd in commands.commands:
                self._commander.execute(cmd)

        return Symbol(self._commander.graph)

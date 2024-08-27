
from graphs.commands.types import AnyCommand
from graphs.utils import StrictModel


class ExecuteCommands(StrictModel):
    commands: list[
        AnyCommand]  # todo maybe limit the ai to 1 command at a time (more expensive, but maybe better (more careful))

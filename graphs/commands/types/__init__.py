from typing import get_args

from graphs.commands.types.add import AddNodesCommand, AddEdgesCommand
from graphs.commands.types.create_types import CreateNodeTypesCommand, CreateEdgeTypesCommand
from graphs.commands.types.delete import DeleteNodesCommand, DeleteEdgesCommand
from graphs.utils import StrictModel

AnyCommand = (CreateNodeTypesCommand | CreateEdgeTypesCommand | AddNodesCommand | AddEdgesCommand | DeleteNodesCommand
              | DeleteEdgesCommand)

commands: tuple[type[StrictModel], ...] = get_args(AnyCommand)

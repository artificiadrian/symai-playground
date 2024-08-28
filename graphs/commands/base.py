from enum import StrEnum
from typing import Literal

from pydantic import Field, create_model

from graphs.utils import StrictModel


class CommandName(StrEnum):
    add_edges = "add_edges"
    delete_edges = "delete_edges"
    add_nodes = "add_nodes"
    delete_nodes = "delete_nodes"
    create_edge_types = "create_edge_types"
    create_node_types = "create_node_types"


class BaseCommand(StrictModel):
    reason: str = Field(..., description="Why was this command executed?")


def create_command_type(type_name: str, command_name: str, description: str, **fields: tuple[type]):
    cls = create_model(type_name, __base__=BaseCommand, cmd=(Literal[command_name],),
                       **fields)
    cls.__doc__ = description
    return cls

from typing import Literal

from pydantic import Field

from graphs.commands.base import BaseCommand, CommandName
from graphs.properties import Property
from graphs.utils import StrictModel


class EdgeTypeDefinition(StrictModel):
    name: str = Field("Type name in PascalCase")
    description: str

    properties: list[Property]

    source: str = Field(description="Name of the source node type in PascalCase")
    target: str = Field(
        description="Name of the target node type in PascalCase")  # TODO maybe dynamically recreate this, too, 
    # and provide options here?


class NodeTypeDefinition(StrictModel):
    name: str = Field("Type name in PascalCase")
    description: str

    properties: list[Property]


class CreateEdgeTypesCommand(BaseCommand):
    cmd: Literal[CommandName.create_edge_types]

    new_types: list[EdgeTypeDefinition]


class CreateNodeTypesCommand(BaseCommand):
    cmd: Literal[CommandName.create_node_types]

    new_types: list[NodeTypeDefinition]

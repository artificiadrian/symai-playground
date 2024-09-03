from pydantic import Field, create_model

from ontology.graphs.properties import Property, create_property_fields
from ontology.utils import StrictModel, literal


class Edge(StrictModel):
    id: str = Field(description="Unique id (in camelCase)")


class EdgeTypeDef(StrictModel):
    name: str = Field(..., description="Type name (in PascalCase)")
    description: str

    properties: list[Property]

    source: str = Field(description="Name of the source node type in PascalCase")
    target: str = Field(
        description="Name of the target node type in PascalCase"
    )  # TODO maybe dynamically recreate this, too, and provide options here?


def create_edge_type(etd: EdgeTypeDef):
    return create_model(
        etd.name,
        __base__=Edge,
        field_definitions={
            "type": (literal(etd.name), Field(default=etd.name)),
            **create_property_fields(etd.properties),
        },
    )

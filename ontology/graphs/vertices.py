from pydantic import Field, create_model

from ontology.graphs.properties import Property, create_property_fields
from ontology.utils import StrictModel


class Vertex(StrictModel):
    id: str = Field(..., description="Unique id (in camelCase)")


class VertexTypeDef(StrictModel):
    name: str = Field(..., description="Type name (in PascalCase)")
    description: str

    properties: list[Property]


def create_vertex_type(vtd: VertexTypeDef):
    x = {
        **create_property_fields(vtd.properties),
    }

    print(x)

    return create_model(
        vtd.name,
        __base__=Vertex,
        **x,
    )

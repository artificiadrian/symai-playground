from pydantic import Field

from ontology.utils import StrictModel


class Vertex(StrictModel):
    id: str = Field(..., description="Globally unique id (camelCase)")

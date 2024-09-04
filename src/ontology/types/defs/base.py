from pydantic import Field

from ontology.types.defs.properties import PropertyDefs
from ontology.utils import StrictModel


class TypeDef(StrictModel):
    name: str = Field(..., description="Name of type (PascalCase)")
    description: str

    props: PropertyDefs

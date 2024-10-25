from dataclasses import dataclass

from ontology.types.defs import NodeTypeDefinition, PropertyDefinition


@dataclass(frozen=True, slots=True)
class EdgeTypeDefinition:
    name: str
    description: str

    source_type: NodeTypeDefinition
    target_type: NodeTypeDefinition

    properties: tuple[PropertyDefinition, ...]

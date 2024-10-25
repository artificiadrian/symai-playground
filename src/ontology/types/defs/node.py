from dataclasses import dataclass

from ontology.types.defs import PropertyDefinition


@dataclass(frozen=True, slots=True)
class IdScheme:
    format: str
    examples: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class NodeTypeDefinition:
    name: str
    description: str

    id_scheme: IdScheme

    properties: tuple[PropertyDefinition, ...]

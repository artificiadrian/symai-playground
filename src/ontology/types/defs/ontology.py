from dataclasses import dataclass

from ontology.types.defs import EdgeTypeDefinition, NodeTypeDefinition


@dataclass(frozen=True, slots=True)
class OntologyTypeDefinition:
    nodes: tuple[NodeTypeDefinition, ...]
    edges: tuple[EdgeTypeDefinition, ...]

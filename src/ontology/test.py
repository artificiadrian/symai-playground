from ontology.types.defs import (
    EdgeTypeDefinition,
    IdScheme,
    NodeTypeDefinition,
    OntologyTypeDefinition,
    ScalarPropertyDefinition,
    ScalarType,
)

paper_node = NodeTypeDefinition(
    name="Paper",
    description="A scientific paper",
    id_scheme=IdScheme(
        format="doi or if not available, title in snake_case",
        examples=("10.1000/xyz123",),
    ),
    properties=(ScalarPropertyDefinition(name="title", type=ScalarType.STRING),),
)

author_node = NodeTypeDefinition(
    name="Author",
    description="An author of a scientific paper",
    id_scheme=IdScheme(
        format="Snake_case! If multiple first names, middle names or last names, append together with underscores.",
        examples=("john_doe",),
    ),
    properties=(
        ScalarPropertyDefinition(
            name="name", description="Name of the author", type=ScalarType.STRING
        ),
    ),
)

concept_node = NodeTypeDefinition(
    name="Concept",
    description="A concept discussed in the paper",
    id_scheme=IdScheme(
        format="conceptid",
        examples=("c12345",),
    ),
    properties=(
        ScalarPropertyDefinition(
            name="description",
            description="Description of the concept",
            type=ScalarType.STRING,
        ),
    ),
)

term_node = NodeTypeDefinition(
    name="Term",
    description="A term used in the paper",
    id_scheme=IdScheme(
        format="Term in snake_case",
        examples=("artificial_intelligence",),
    ),
    properties=(
        ScalarPropertyDefinition(
            name="term", description="Term used in the paper", type=ScalarType.STRING
        ),
    ),
)

authorship_edge = EdgeTypeDefinition(
    name="Authorship",
    description="Links a paper to its authors",
    source_type=paper_node,
    target_type=author_node,
    properties=(),
)

conceptual_edge = EdgeTypeDefinition(
    name="Conceptual",
    description="Links a paper to the concepts it discusses",
    source_type=paper_node,
    target_type=concept_node,
    properties=(),
)

terminology_edge = EdgeTypeDefinition(
    name="Terminology",
    description="Links a paper to the terms it uses",
    source_type=paper_node,
    target_type=term_node,
    properties=(),
)

ontology = OntologyTypeDefinition(
    nodes=(paper_node, author_node, concept_node, term_node),
    edges=(authorship_edge, conceptual_edge, terminology_edge),
)

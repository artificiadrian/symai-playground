from pydantic import create_model

from ontology.types.defs.base import TypeDef
from ontology.types.defs.properties import create_property_kwargs
from ontology.types.vertices import Vertex


class VertexTypeDef(TypeDef):
    pass


def create_vertex_type(vtd: VertexTypeDef):
    props = create_property_kwargs(vtd.props)

    # TODO contextualize these errors, add custom exception types

    if "id" in props:
        raise ValueError("Cannot define a property named 'id'")

    cls = create_model(vtd.name, __base__=Vertex, **props)

    cls.__doc__ = vtd.description

    return cls

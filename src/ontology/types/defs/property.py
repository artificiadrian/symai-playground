from dataclasses import dataclass, field
from enum import StrEnum


class ScalarType(StrEnum):
    STRING = "STRING"
    INT = "INT"
    BOOLEAN = "BOOLEAN"


@dataclass(frozen=True, slots=True)
class PropertyDefinitionBase:
    name: str
    description: str | None = field(default=None, kw_only=True)


@dataclass(frozen=True, slots=True)
class ScalarPropertyDefinition(PropertyDefinitionBase):
    type: ScalarType


PropertyDefinition = ScalarPropertyDefinition

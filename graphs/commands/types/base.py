from dataclasses import dataclass

from create_type_system import Field
from graphs.utils import StrictModel


class BaseCommand(StrictModel):
    reason: str = Field(..., description="Why was this command executed?")


@dataclass(frozen=True, slots=True)
class CommandInfo:
    description: str

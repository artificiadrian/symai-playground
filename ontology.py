import json

from pydantic import BaseModel

from typing import TypeVar

from symai import Symbol
from symai.components import FunctionWithUsage

from schema import TypeSystem

T = TypeVar('T', bound=BaseModel)

prompt = """I want to create a type system to extract structured information from the given sample text. My goal is 
to {goal}. \nPlease respond with a type system defined as a JSON object that adheres to the given schema.\n\nAs an 
additional aide, I provide some sample text further down. The type system needs to adhere to the GOAL but NOT TO THE 
SAMPLE TEXT."""


class CreateTypeSystem(FunctionWithUsage):
    def __init__(self, goal: str, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         static_context=prompt.format(goal=goal),
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "type",
                             "schema": TypeSystem.model_json_schema()
                         }})


with open("examples/data/reddit_wp.txt", "rb") as f:
    text = Symbol(f.read().decode())

create_type_system = CreateTypeSystem("build a character relationship diagram.")
res: Symbol = create_type_system(text)
print(json.dumps(json.loads(res[0]), indent=True))

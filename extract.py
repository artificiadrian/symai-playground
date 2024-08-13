from symai import Symbol
from symai.components import FunctionWithUsage

from utils import ModelT, Model


class Character(Model):
    name: str
    description: str


class CharacterList(Model):
    characters: list[Character]


extract_prompt = ("You are a data scientist tasked with extracting structured information from a given sample text. "
                  "You have been provided with a sample text and a JSON object schema. Please respond with a JSON "
                  "object that adheres to the provided schema and contains the extracted information.")


# open questions: 
# - how to have references between entities? e.g. character relationshop diagram.
#    this is tricky because it's a chicken and egg problem. 

# what about circular references? character with list of friends?
# can llm provide deterministic object keys s.t. we can merge manually?

class Extract(FunctionWithUsage):

    def __init__(self, type: type[ModelT], prompt=extract_prompt, *args, **kwargs):
        self._extract_type = type
        super().__init__(*args, **kwargs, static_context=prompt,
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "extracted_information",
                             "schema": type.model_json_schema()
                         }})

    def forward(self, *args, **kwargs):
        x = super().forward(*args, **kwargs)
        return self._extract_type.model_validate_json(x[0]), x[1]


with open("examples/data/facts.txt", "rb") as f:
    symbol = Symbol(f.read().decode())

extract = Extract(CharacterList)
print(extract(symbol))

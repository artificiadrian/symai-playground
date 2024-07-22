from pydantic import BaseModel, Field
from symai import Symbol

from ontology import ExtractObject


class Book(BaseModel):
    title: str
    description: str | None = Field(None, description="A short description of the book. Just a few words.")
    genre: str = Field(None, description="Try to guess this from the description and title!")


class Author(BaseModel):
    full_name: str
    age: int
    books: list[Book]
    life: str | None = Field(None, description="A short summary of the author's life.")


with open("david_deutsch_wiki.txt", "rb") as f:
    text = f.read().decode("utf-8")

extract = ExtractObject(Author)
result = extract(Symbol(text), max_tokens=2800)
print(result.value.model_dump_json(indent=True), type(result.value))

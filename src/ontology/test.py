import os
from pathlib import Path

import openai
import tiktoken
from pydantic import Field

from ontology.utils import StrictModel

dotenv = Path(".env").read_text()
for line in dotenv.splitlines():
    key, value = line.split("=")
    os.environ[key] = value

if not os.environ["OPENAI_API_KEY"]:
    raise Exception("OPENAI_API_KEY environment variable not set")

text = Path("examples/wikipedia_ww2.txt").read_text(encoding="utf-8")

encoding = tiktoken.get_encoding("cl100k_base")


def chunked(text: str, chunk_size: int = 128_000):
    tokens = encoding.encode(text)
    for i in range(0, len(tokens), chunk_size):
        yield encoding.decode(tokens[i: i + chunk_size])


class Person(StrictModel):
    id: str = Field(
        ...,
        description="{fname}_{lname} (snake_case!) (e.g. 'john_doe', 'jane_smith')",
    )

    first_name: str
    last_name: str
    description: str



for chunk in chunked(text):
    resp = openai.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract ALL relevant information from the text",
            },
            {"role": "user", "content": chunk},
        ],
        response_format=AddPersons,
    )

    print(resp.choices[0].message.parsed)

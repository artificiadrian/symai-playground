from typing import TypeVar, Generic

from pydantic import BaseModel, Field
from symai import Expression, Symbol

T = TypeVar('T', bound=BaseModel)


class ExtractObject(Expression, Generic[T]):

    def __init__(self, dtype: type[T],
                 system_prompt: str = "You are a grade-A researcher, tasked with extracting information from raw text. You do not make up examples and always stick to the facts that are present in the text.\nYou are given a JSON schema to follow. Construct a JSON object from the given text.",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_prompt = system_prompt
        self.dtype = dtype

    def forward(self, symbol: Symbol, *args, **kwargs):
        res = Expression.prompt(
            message=[
                {"role": "system",
                 "content": self.system_prompt},
                {"role": "user", "content": f"Schema: {self.dtype.model_json_schema()}"},
                {"role": "system", "content": f"Text: {symbol}"}
            ],
            response_format={"type": "json_object"}
        )

        return Symbol(self.dtype.model_validate_json(res.value))




from symai.components import FunctionWithUsage

from utils import Model

refine_prompt_prompt = ("You are a world-renowed expert in prompt engineering. You have been tasked with refining the "
                        "following prompt to improve performance when input to LLMs. Please respond with a JSON "
                        "object that adheres "
                        "to the provided schema. Also, make sure that the refined prompt still adheres to the "
                        "original goal.")


class RefinedPrompt(Model):
    refined_prompt: str
    reasoning: list[str]


# TODO this does not work very well so far!

class RefinePrompt(FunctionWithUsage):
    """Refines a prompt to make it more effective and to optionally adhere to a specific goal."""

    def __init__(self, additional_goal: str = None):
        prompt = refine_prompt_prompt if additional_goal is None else refine_prompt_prompt + (
            f"\n\nAdditional new goal: "
            f"{additional_goal}")
        super().__init__(static_context=prompt,
                         response_format={"type": "json_schema", "json_schema": {
                             "strict": True,
                             "name": "refined_prompt",
                             "schema": RefinedPrompt.model_json_schema()
                         }})

    def forward(self, *args, **kwargs):
        x = super().forward(*args, **kwargs)
        return RefinedPrompt.model_validate_json(x[0]), x[1]

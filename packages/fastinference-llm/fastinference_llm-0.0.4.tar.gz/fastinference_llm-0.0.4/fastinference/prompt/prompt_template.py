from typing import List, Dict


class PromptTemplate:
    def __init__(self, data, core_prompt: str):
        self.data = data
        self.core_prompt = core_prompt
        self.prompt = self.render_prompt()

    def render_prompt(self) -> str:
        try:
            format_dict = {'content': self.data.content, **self.data.metadata}
            return self.core_prompt.format(**format_dict)
        except KeyError as e:
            raise ValueError(f"Missing variable {e} in the prompt template.")

    def render_prompt_for_litellm(self) -> List[Dict]:
        try:
            return [{"content": self.prompt, "role": "user"}]
        except Exception as e:
            raise Exception(f'Could not convert the prompt in the litellm format: {e}')
import backoff
import openai

from litellm import acompletion
from typing import List, Dict
from fastinference.data_processing.datablock import DataBlock


class LLMManager:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    @backoff.on_exception(backoff.expo,
                          (openai.APITimeoutError,
                           openai.BadRequestError,
                           openai.AuthenticationError,
                           openai.PermissionDeniedError,
                           openai.NotFoundError,
                           openai.UnprocessableEntityError,
                           openai.RateLimitError),
                          max_time=300)
    async def acompletions_with_backoff(self, data: DataBlock, **kwargs):
        extract_content_with_prompt = data.content_with_prompt.render_prompt_for_litellm()
        data.response = await acompletion(**self.__dict__, **kwargs, messages=extract_content_with_prompt)
        return data

    async def get_acompletion(self, content: DataBlock):
        return await self.acompletions_with_backoff(data=content)
        

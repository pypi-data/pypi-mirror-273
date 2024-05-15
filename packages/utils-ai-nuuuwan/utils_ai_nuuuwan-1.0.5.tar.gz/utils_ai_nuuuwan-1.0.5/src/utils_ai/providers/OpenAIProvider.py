import os

import openai

from utils_ai.generic_ai import GenericAI


class OpenAIProvider(GenericAI):
    NAME = 'OpenAI'
    MODEL = 'gpt-4'
    IMAGE_MODEL = 'dall-e-3'

    def __init__(self):
        GenericAI.__init__(self)

        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def get_chat_reply(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=OpenAIProvider.MODEL, messages=messages
        )
        return response.choices[0].message.content

    def get_image_url(self, prompt: str) -> str:
        response = self.client.images.generate(
            model=OpenAIProvider.IMAGE_MODEL,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url

import os

from mistralai.client import MistralClient

from utils_ai.generic_ai import GenericAI


class MistralAIProvider(GenericAI):
    NAME = 'MistralAI'
    MODEL = 'mistral-large-latest'

    def __init__(self):
        GenericAI.__init__(self)

        self.client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))

    def get_chat_reply(self, messages: list) -> str:
        response = self.client.chat(
            model=MistralAIProvider.MODEL, messages=messages
        )
        return response.choices[0].message.content

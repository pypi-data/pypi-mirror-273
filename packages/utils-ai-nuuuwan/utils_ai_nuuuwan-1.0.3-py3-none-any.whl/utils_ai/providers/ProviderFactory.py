import random

from utils_ai.providers.MistralAIProvider import MistralAIProvider
from utils_ai.providers.OpenAIProvider import OpenAIProvider


class ProviderFactory:
    PROVIDER_LIST = [
        OpenAIProvider,
        MistralAIProvider,
    ]

    @staticmethod
    def random():
        provider = random.choice(ProviderFactory.PROVIDER_LIST)
        return provider()

    @staticmethod
    def from_name(name: str):
        if name == OpenAIProvider.NAME:
            return OpenAIProvider()
        if name == MistralAIProvider.NAME:
            return MistralAIProvider()
        raise ValueError(f'Unknown provider name: {name}')

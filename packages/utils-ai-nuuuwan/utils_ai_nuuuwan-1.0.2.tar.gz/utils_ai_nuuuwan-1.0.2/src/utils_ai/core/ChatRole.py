from enum import Enum


class ChatRole(str, Enum):
    user = 'user'
    system = 'system'  # noqa
    assistant = 'assistant'
    function = 'function'  # noqa

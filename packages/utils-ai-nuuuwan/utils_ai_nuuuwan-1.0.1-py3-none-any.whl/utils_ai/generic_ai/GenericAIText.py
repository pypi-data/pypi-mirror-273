from utils_base import Log

from utils_ai.core.ChatRole import ChatRole
from utils_ai.core.Message import Message

log = Log('AIChat')


class GenericAIText:
    def __init__(self):
        self.messages = []

    def append_message(self, role: ChatRole, content: str):
        self.messages.append(Message(role=role, content=content).todict())

    def get_chat_reply(self, messages: list) -> str:
        raise NotImplementedError

    def chat(self, message: str) -> str:
        self.append_message(ChatRole.user, message)
        reply = self.get_chat_reply(self.messages)
        self.append_message(ChatRole.assistant, reply)
        return reply

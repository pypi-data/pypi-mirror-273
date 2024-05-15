from utils_base import Log

from utils_ai.core.ChatRole import ChatRole
from utils_ai.core.Message import Message

log = Log('GenericAIText')


class GenericAIText:
    def __init__(self):
        self.messages = []

    def set_profile(self, profile_content: str):
        self.messages.append(
            Message(role=ChatRole.system, content=profile_content).todict()
        )

    def append_message(self, role: ChatRole, content: str):
        self.messages.append(Message(role=role, content=content).todict())

    def get_chat_reply(self, messages: list) -> str:
        raise NotImplementedError

    def chat(self, message: str) -> str:
        self.append_message(ChatRole.user, message)
        try:
            reply = self.get_chat_reply(self.messages)
            self.append_message(ChatRole.assistant, reply)
            return reply
        except Exception as e:
            log.error(str(e))
            return None

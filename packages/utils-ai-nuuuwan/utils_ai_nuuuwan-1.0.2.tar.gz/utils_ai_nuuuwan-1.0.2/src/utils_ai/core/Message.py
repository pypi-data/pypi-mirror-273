from attr import dataclass

from utils_ai.core.ChatRole import ChatRole


@dataclass
class Message:
    role: ChatRole
    content: str

    def todict(self):
        return dict(role=self.role, content=self.content)

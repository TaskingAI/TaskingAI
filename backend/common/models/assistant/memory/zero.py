from ._base import *
from ._utils import message_role_to_memory_role


class ChatZeroMemory(ChatMemory):
    type: MemoryType = Field(MemoryType.zero, Literal=MemoryType.zero, description="The type of the memory.")

    async def update_memory(self, new_message: Message):
        messages = self.messages
        role: ChatMemoryMessageRole = message_role_to_memory_role(new_message.role)
        if role == ChatMemoryMessageRole.user:
            # add message
            return ChatZeroMemory(
                messages=[*messages, ChatMemoryMessage(role=role, content=new_message.content["text"])]
            )
        elif role == ChatMemoryMessageRole.assistant:
            # clean message
            return ChatZeroMemory()


class AssistantZeroMemory(AssistantMemory):
    type: MemoryType = Field(MemoryType.zero, Literal=MemoryType.zero, description="The type of the memory.")

    def init_chat_memory(self) -> ChatZeroMemory:
        return ChatZeroMemory()

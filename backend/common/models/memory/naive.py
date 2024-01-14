from ._base import *
from ._utils import message_role_to_memory_role
from pydantic import Field


class ChatNaiveMemory(ChatMemory):
    type: MemoryType = Field(MemoryType.naive, Literal=MemoryType.naive, description="The type of the memory.")

    async def update_memory(self, new_message: Message):
        messages = self.messages
        role = message_role_to_memory_role(new_message.role)
        return ChatNaiveMemory(messages=[*messages, ChatMemoryMessage(role=role, content=new_message.content["text"])])


class AssistantNaiveMemory(AssistantMemory):
    type: MemoryType = Field(MemoryType.naive, Literal=MemoryType.naive, description="The type of the memory.")

    def init_chat_memory(self) -> ChatNaiveMemory:
        return ChatNaiveMemory()

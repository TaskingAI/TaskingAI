from ._base import *
from pydantic import Field


class ChatNaiveMemory(ChatMemory):
    type: MemoryType = Field(MemoryType.naive, Literal=MemoryType.naive, description="The type of the memory.")

    async def update_memory(self, new_message_text: str, role: str):
        return ChatNaiveMemory(messages=[*self.messages, ChatMemoryMessage(role=role, content=new_message_text)])


class AssistantNaiveMemory(AssistantMemory):
    type: MemoryType = Field(MemoryType.naive, Literal=MemoryType.naive, description="The type of the memory.")

    def init_chat_memory(self) -> ChatNaiveMemory:
        return ChatNaiveMemory()

from ._base import *


class ChatZeroMemory(ChatMemory):
    type: MemoryType = Field(MemoryType.zero, Literal=MemoryType.zero, description="The type of the memory.")

    async def update_memory(self, new_message_text: str, new_message_token_count: int, role: str):
        messages = self.messages
        if role == "user":
            # add message
            return ChatZeroMemory(messages=[*messages, ChatMemoryMessage(role=role, content=new_message_text)])
        elif role == "assistant":
            # clean message
            return ChatZeroMemory()


class AssistantZeroMemory(AssistantMemory):
    type: MemoryType = Field(MemoryType.zero, Literal=MemoryType.zero, description="The type of the memory.")

    def init_chat_memory(self) -> ChatZeroMemory:
        return ChatZeroMemory()

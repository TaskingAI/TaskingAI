from ._base import *
from ._utils import count_tokens


class ChatMessageWindowMemory(ChatMemory):
    type: MemoryType = Field(
        MemoryType.message_window, Literal=MemoryType.message_window, description="The type of the memory."
    )
    max_messages: int = Field(
        ...,
        ge=1,
        le=1024,
        description="The maximum number of recent messages (from both the user and assistant) that can be remembered.",
    )
    max_tokens: int = Field(
        ...,
        ge=1,
        le=8192,
        description="The total limit on the number of tokens the assistant can retain across the recent messages.",
    )

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "messages": [message.model_dump() for message in self.messages],
            "max_messages": self.max_messages,
            "max_tokens": self.max_tokens,
        }

    async def update_memory(self, new_message_text: str, role: str):
        messages = self.messages
        max_messages = self.max_messages
        max_tokens = self.max_tokens

        # Calculate token count for new message
        new_message_token_count = count_tokens(new_message_text)

        # Add new message to the memory
        messages.append(ChatMemoryMessage(role=role, content=new_message_text, token_count=new_message_token_count))

        # Trim messages to ensure they don't exceed max_messages or max_tokens
        if role == "assistant":
            total_tokens = sum(message.token_count for message in messages)
            while len(messages) > max_messages or total_tokens > max_tokens:
                removed_message = messages.pop(0)
                total_tokens -= removed_message.token_count

        return ChatMessageWindowMemory(messages=messages, max_messages=self.max_messages, max_tokens=self.max_tokens)


class AssistantMessageWindowMemory(AssistantMemory):
    type: MemoryType = Field(
        MemoryType.message_window, Literal=MemoryType.message_window, description="The type of the memory."
    )
    max_messages: int = Field(
        ...,
        ge=1,
        le=1024,
        description="The maximum number of recent messages (from both the user and assistant) that can be remembered.",
    )
    max_tokens: int = Field(
        ...,
        ge=1,
        le=8192,
        description="The total limit on the number of tokens the assistant can retain across the recent messages.",
    )

    def init_chat_memory(self) -> ChatMessageWindowMemory:
        return ChatMessageWindowMemory(max_messages=self.max_messages, max_tokens=self.max_tokens)

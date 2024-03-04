from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict, List
from tkhelper.error import raise_http_error, ErrorCode

from .assistant_memory import MemoryType


class ChatMemoryMessage(BaseModel):
    role: str = Field(..., description="The role of the message.")
    content: str = Field(..., description="The text content of the message.")
    token_count: Optional[int] = Field(None, description="The number of tokens in the message.")

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        if self.token_count is not None:
            return {"role": self.role, "content": self.content, "token_count": self.token_count}
        else:
            return {"role": self.role, "content": self.content}


class ChatMemory(BaseModel):
    type: MemoryType = Field(..., description="The type of the memory.")
    messages: List[ChatMemoryMessage] = Field([], description="The list of messages in the memory.")
    max_messages: Optional[int] = Field(
        None,
        ge=1,
        le=1024,
        description="The maximum number of recent messages (from both the user and assistant) that can be remembered.",
    )
    max_tokens: Optional[int] = Field(
        None,
        ge=1,
        le=8192,
        description="The total limit on the number of tokens the assistant can retain across the recent messages.",
    )

    @field_validator("messages", mode="after")
    def validate_messages(cls, messages: List[ChatMemoryMessage]):
        # the total char of all messages cannot be longer than 65535
        total_char = [len(message.content) for message in messages]
        if sum(total_char) > 65535:
            raise_http_error(
                ErrorCode.RESOURCE_LIMIT_REACHED,
                "The total number of characters in all the memory messages cannot be larger than 65535.",
            )
        return messages

    async def update_memory(
        self,
        new_message_text: str,
        role: str,
        new_message_token_count: int,
    ):
        messages = self.messages
        max_messages = self.max_messages
        max_tokens = self.max_tokens

        if self.type == MemoryType.naive:
            return ChatMemory(
                type=self.type, messages=[*self.messages, ChatMemoryMessage(role=role, content=new_message_text)]
            )

        elif self.type == MemoryType.zero:
            if role == "user":
                # add message
                return ChatMemory(
                    type=self.type, messages=[*messages, ChatMemoryMessage(role=role, content=new_message_text)]
                )
            elif role == "assistant":
                # clean message
                return ChatMemory(type=self.type)

        elif self.type == MemoryType.message_window:
            # Add new message to the memory
            messages.append(ChatMemoryMessage(role=role, content=new_message_text, token_count=new_message_token_count))

            # Trim messages to ensure they don't exceed max_messages or max_tokens
            if role == "assistant":
                total_tokens = sum(message.token_count for message in messages)
                while len(messages) > max_messages or total_tokens > max_tokens:
                    removed_message = messages.pop(0)
                    total_tokens -= removed_message.token_count

            return ChatMemory(
                type=self.type, messages=messages, max_messages=self.max_messages, max_tokens=self.max_tokens
            )

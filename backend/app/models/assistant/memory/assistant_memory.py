from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Optional

__all__ = ["MemoryType", "AssistantMemory"]


class MemoryType(str, Enum):
    zero = "zero"
    naive = "naive"
    message_window = "message_window"


class AssistantMemory(BaseModel):
    type: MemoryType = Field(
        ...,
        description="The type of the memory.",
    )

    max_messages: Optional[int] = Field(
        None,
        ge=1,
        le=1024,
        description="The maximum number of recent messages (from both the user and assistant) that can be remembered. "
        "It is required for the message_window memory type.",
    )

    max_tokens: Optional[int] = Field(
        None,
        ge=1,
        le=8192,
        description="The total limit on the number of tokens the assistant can retain across the recent messages. "
        "It is required for the message_window memory type.",
    )

    @model_validator(mode="after")
    def validate(self):
        if self.type == MemoryType.message_window and (self.max_messages is None):
            raise ValueError("the max_messages field is required for the message_window memory type.")
        return self

    def init_chat_memory(self):
        from .chat_memory import ChatMemory

        if self.type == MemoryType.naive:
            return ChatMemory(type=self.type)

        elif self.type == MemoryType.zero:
            return ChatMemory(type=self.type)

        if self.type == MemoryType.message_window:
            return ChatMemory(type=self.type, max_messages=self.max_messages, max_tokens=self.max_tokens)

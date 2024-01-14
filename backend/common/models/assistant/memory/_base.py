from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict, List
from abc import ABC, abstractmethod
from common.models import Message
from common.error import raise_http_error, ErrorCode


class MemoryType(str, Enum):
    zero = "zero"
    naive = "naive"
    message_window = "message_window"


class AssistantMemory(BaseModel, ABC):
    type: MemoryType = Field(..., description="The type of the memory.")

    @abstractmethod
    def init_chat_memory(self):
        raise NotImplementedError


class ChatMemoryMessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class ChatMemoryMessage(BaseModel):
    role: ChatMemoryMessageRole = Field(..., description="The role of the message.")
    content: str = Field(..., description="The text content of the message.")
    token_count: Optional[int] = Field(None, description="The number of tokens in the message.")

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        if self.token_count is not None:
            return {"role": self.role.value, "content": self.content, "token_count": self.token_count}
        else:
            return {"role": self.role.value, "content": self.content}


class ChatMemory(BaseModel, ABC):
    type: MemoryType = Field(..., description="The type of the memory.")
    messages: List[ChatMemoryMessage] = Field([], description="The list of messages in the memory.")

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return {"type": self.type.value, "messages": [message.model_dump() for message in self.messages]}

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

    @abstractmethod
    async def update_memory(self, new_message: Message):
        raise NotImplementedError

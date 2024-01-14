from pydantic import BaseModel, Field
from enum import Enum
from common.utils import generate_random_id, load_json_attr
from typing import Dict, Optional
from .base import SerializePurpose

__all__ = ["Message", "MessageRole", "MessageContent"]


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class MessageContent(BaseModel):
    text: Optional[str] = Field(None, description="The text content of the message.", examples=["Hello!"])

    # todo: support more content type, i.e. file, image, etc.


class Message(BaseModel):
    message_id: str
    chat_id: str
    assistant_id: str
    role: MessageRole
    content: MessageContent
    metadata: Dict
    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def object_name():
        return "Message"

    @staticmethod
    def generate_random_id():
        return "Mah1" + generate_random_id(20)

    @classmethod
    def build(cls, row):
        return cls(
            message_id=row["message_id"],
            chat_id=row["chat_id"],
            assistant_id=row["assistant_id"],
            role=MessageRole(row["role"]),
            content=MessageContent(**load_json_attr(row, "content", {})),
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        ret = {
            "object": self.object_name(),
            "message_id": self.message_id,
            "chat_id": self.chat_id,
            "assistant_id": self.assistant_id,
            "role": self.role.value,
            "content": self.content,
            "metadata": self.metadata,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }
        return ret

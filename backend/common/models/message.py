from pydantic import BaseModel
from enum import Enum
from common.utils import generate_random_id
from typing import Dict
import json
from .base import SerializePurpose


__all__ = ["Message", "MessageRole"]


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    message_id: str
    chat_id: str
    assistant_id: str
    role: MessageRole
    content: Dict
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
            message_id=row.message_id,
            chat_id=row.chat_id,
            assistant_id=row.assistant_id,
            role=row.role,
            content=json.loads(row.content),
            metadata=json.loads(row.metadata),
            created_timestamp=row.created_timestamp,
            configs=json.loads(row.configs) if row.configs else None,
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
            "created_timestamp": self.created_timestamp,
        }
        return ret

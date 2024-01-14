from common.utils import generate_random_id
from pydantic import BaseModel
from typing import Dict
from .base import SerializePurpose
from common.utils import generate_random_id, load_json_attr


class Chat(BaseModel):
    chat_id: str
    assistant_id: str
    metadata: Dict
    memory: Dict
    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def object_name():
        return "Chat"

    @staticmethod
    def generate_random_id():
        return "SdEL" + generate_random_id(20)

    @classmethod
    def build(cls, row):
        return cls(
            chat_id=row["chat_id"],
            assistant_id=row["assistant_id"],
            memory=load_json_attr(row, "memory", {}),
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        return {
            "object": self.object_name(),
            "chat_id": self.chat_id,
            "assistant_id": self.assistant_id,
            "memory": self.memory,
            "metadata": self.metadata,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

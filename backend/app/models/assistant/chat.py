from typing import Dict, List

from pydantic import Field

from tkhelper.models import ModelEntity
from tkhelper.utils import load_json_attr, generate_random_id
from tkhelper.schemas.field import *

from app.database import redis_conn
from .assistant import Assistant
from .memory import ChatMemory

__all__ = ["Chat"]


class Chat(ModelEntity):
    object: str = "Chat"
    assistant_id: str = id_field("assistant", length=24)
    chat_id: str = id_field("chat", length=24)

    metadata: Dict = metadata_field()
    memory: ChatMemory = Field(...)
    name: str = name_field("chat")

    created_timestamp: int = created_timestamp_field()
    updated_timestamp: int = updated_timestamp_field()

    @staticmethod
    def build(row):
        return Chat(
            # ids
            chat_id=row["chat_id"],
            assistant_id=row["assistant_id"],
            # data
            memory=load_json_attr(row, "memory", {}),
            metadata=load_json_attr(row, "metadata", {}),
            name=row.get("name") or "",
            # timestamps
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_response_dict(self) -> Dict:
        return {
            "object": "Chat",
            "assistant_id": self.assistant_id,
            "chat_id": self.chat_id,
            "metadata": self.metadata,
            "memory": self.memory,
            "name": self.name,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }

    @staticmethod
    def object_name() -> str:
        return "chat"

    @staticmethod
    def object_plural_name() -> str:
        return "chats"

    @staticmethod
    def table_name() -> str:
        return "chat"

    @staticmethod
    def id_field_name() -> str:
        return "chat_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["assistant_id", "chat_id"]

    @staticmethod
    def generate_random_id(**kwargs) -> str:
        return "SdEL" + generate_random_id(20)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return []

    @staticmethod
    def parent_models() -> List:
        return [Assistant]

    @staticmethod
    def parent_operator() -> List:
        from app.operators import assistant_ops

        return [assistant_ops]

    @staticmethod
    def create_fields() -> List[str]:
        return ["metadata", "name"]

    @staticmethod
    def update_fields() -> List[str]:
        return ["metadata", "name"]

    @staticmethod
    def fields_exclude_in_response():
        return []

    def __lock_redis_key(self):
        return f"chat:{self.assistant_id}:{self.chat_id}:lock"

    async def is_chat_locked(self):
        return await redis_conn.get_int(key=self.__lock_redis_key()) == 1

    async def lock(self):
        await redis_conn.set_int(key=self.__lock_redis_key(), value=1, expire=120)

    async def unlock(self):
        await redis_conn.pop(key=self.__lock_redis_key())

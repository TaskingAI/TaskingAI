from common.utils import generate_random_id
from pydantic import BaseModel
from typing import Dict
from common.models import SerializePurpose
from .memory import ChatMemory, build_chat_memory
from common.utils import generate_random_id, load_json_attr
from common.database.redis import redis_object_pop, redis_object_set_object, redis_object_get_object


class Chat(BaseModel):
    chat_id: str
    assistant_id: str
    metadata: Dict
    memory: ChatMemory
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
        memory_dict = load_json_attr(row, key="memory", default_value={"messages": [], "context_summary": None})
        chat_memory: ChatMemory = build_chat_memory(memory_dict)
        return cls(
            chat_id=row["chat_id"],
            assistant_id=row["assistant_id"],
            memory=chat_memory,
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        return {
            "object": self.object_name(),
            "chat_id": self.chat_id,
            "assistant_id": self.assistant_id,
            "memory": self.memory.model_dump(exclude_none=True),
            "metadata": self.metadata,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

    @classmethod
    async def get_redis(cls, assistant_id: str, chat_id: str):
        return await redis_object_get_object(
            Chat,
            key=f"{assistant_id}:{chat_id}",
        )

    async def set_redis(self):
        await redis_object_set_object(
            Chat,
            key=f"{self.assistant_id}:{self.chat_id}",
            value=self.to_dict(purpose=SerializePurpose.REDIS),
        )

    async def pop_redis(self):
        await redis_object_pop(
            Chat,
            key=f"{self.assistant_id}:{self.chat_id}",
        )

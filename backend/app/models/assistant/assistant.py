from typing import Dict, List

from pydantic import Field

from tkhelper.models import ModelEntity
from tkhelper.utils import load_json_attr, generate_random_id
from tkhelper.schemas.field import *

from .memory import AssistantMemory
from ..tool.tool import *
from ..retrieval.retrieval import *

__all__ = ["Assistant"]


class Assistant(ModelEntity):
    object: str = "Assistant"
    assistant_id: str = id_field("assistant", length_range=(1, 50))

    model_id: str = id_field("model", length=8)
    name: str = name_field()
    description: str = description_field()

    system_prompt_template: List[str] = Field([])
    memory: AssistantMemory = Field(...)

    tools: List[ToolRef] = Field([])
    # todo: tool_configs: Dict
    retrievals: List[RetrievalRef] = Field([])
    retrieval_configs: RetrievalConfig = Field(...)

    metadata: Dict = metadata_field()
    num_chats: int = Field(0, ge=0, description="The number of chats using this assistant", exclude=True)

    created_timestamp: int = created_timestamp_field()
    updated_timestamp: int = updated_timestamp_field()

    @staticmethod
    def build(row):
        return Assistant(
            assistant_id=row["assistant_id"],
            model_id=row["model_id"],
            name=row["name"],
            description=row["description"],
            system_prompt_template=load_json_attr(row, "system_prompt_template", []),
            memory=load_json_attr(row, "memory", {"type": "zero"}),
            tools=load_json_attr(row, "tools", []),
            retrievals=load_json_attr(row, "retrievals", []),
            retrieval_configs=RetrievalConfig(**load_json_attr(row, "retrieval_configs", {})),
            metadata=load_json_attr(row, "metadata", {}),
            num_chats=row["num_chats"],
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_response_dict(self) -> Dict:
        return {
            "object": "Assistant",
            "assistant_id": self.assistant_id,
            "model_id": self.model_id,
            "name": self.name,
            "description": self.description,
            "system_prompt_template": self.system_prompt_template,
            "memory": self.memory.model_dump(exclude_none=True),
            "tools": [tool.model_dump() for tool in self.tools],
            "retrievals": [retrieval.model_dump() for retrieval in self.retrievals],
            "retrieval_configs": self.retrieval_configs.model_dump(exclude_none=True),
            "metadata": self.metadata,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }

    @staticmethod
    def object_name() -> str:
        return "assistant"

    @staticmethod
    def object_plural_name() -> str:
        return "assistants"

    @staticmethod
    def table_name() -> str:
        return "assistant"

    @staticmethod
    def id_field_name() -> str:
        return "assistant_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["assistant_id"]

    @staticmethod
    def generate_random_id() -> str:
        return "X5lM" + generate_random_id(20)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return ["assistant_id", "name"]

    @staticmethod
    def parent_models() -> List:
        return []

    @staticmethod
    def parent_operator() -> List:
        return []

    @staticmethod
    def create_fields() -> List[str]:
        return [
            "model_id",
            "name",
            "description",
            "system_prompt_template",
            "memory",
            "tools",
            "retrievals",
            "retrieval_configs",
            "metadata",
        ]

    @staticmethod
    def update_fields() -> List[str]:
        return [
            "model_id",
            "name",
            "description",
            "system_prompt_template",
            "memory",
            "tools",
            "retrievals",
            "retrieval_configs",
            "metadata",
        ]

    @staticmethod
    def fields_exclude_in_response():
        return ["num_chats"]

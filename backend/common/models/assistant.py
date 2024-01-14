from common.utils import generate_random_id, load_json_attr
from pydantic import BaseModel, Field
from typing import Dict, List
from .base import SerializePurpose

__all__ = [
    "Assistant",
    "AssistantTool",
]


class AssistantTool(BaseModel):
    type: str = Field(..., description="The tool type, which can be `function` or `action`.", examples=["action"])
    id: str = Field(..., description="The tool ID.", examples=["action_1"])


class Assistant(BaseModel):
    assistant_id: str
    model_id: str
    name: str
    description: str
    system_prompt_template: List[str]
    memory: Dict

    tools: List
    tool_configs: Dict
    retrievals: List
    retrieval_configs: Dict

    metadata: Dict

    created_timestamp: int
    updated_timestamp: int

    @staticmethod
    def object_name():
        return "Assistant"

    @staticmethod
    def generate_random_id():
        return "X5lM" + generate_random_id(20)

    @classmethod
    def build(cls, row: Dict):
        return cls(
            assistant_id=row["assistant_id"],
            model_id=row["model_id"],
            name=row["name"],
            description=row["description"],
            system_prompt_template=load_json_attr(row, "system_prompt_template", []),
            memory=load_json_attr(row, "memory", {}),
            tools=load_json_attr(row, "tools", []),
            tool_configs=load_json_attr(row, "tool_configs", {}),
            retrievals=load_json_attr(row, "retrievals", []),
            retrieval_configs=load_json_attr(row, "retrieval_configs", {}),
            metadata=load_json_attr(row, "metadata", {}),
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        ret = {
            "object": self.object_name(),
            "assistant_id": self.assistant_id,
            "model_id": self.model_id,
            "name": self.name,
            "description": self.description,
            "system_prompt_template": self.system_prompt_template,
            "memory": self.memory,
            "metadata": self.metadata,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
        return ret

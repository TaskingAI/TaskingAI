from common.utils import generate_random_id, load_json_attr
from pydantic import BaseModel, Field
from typing import Dict, List
from common.models import SerializePurpose
from .assistant_retrieval import AssistantRetrieval, AssistantRetrievalConfig
from .memory import AssistantMemory, build_assistant_memory

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
    memory: AssistantMemory

    tools: List[AssistantTool]
    # todo: tool_configs: Dict
    retrievals: List[AssistantRetrieval]
    retrieval_configs: AssistantRetrievalConfig

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
        memory_dict = load_json_attr(row, "memory", {})
        memory = build_assistant_memory(memory_dict)
        return cls(
            assistant_id=row["assistant_id"],
            model_id=row["model_id"],
            name=row["name"],
            description=row["description"],
            system_prompt_template=load_json_attr(row, "system_prompt_template", []),
            memory=memory,
            tools=load_json_attr(row, "tools", []),
            # todo: tool_configs=load_json_attr(row, "tool_configs", {}),
            retrievals=load_json_attr(row, "retrievals", []),
            retrieval_configs=AssistantRetrievalConfig(**load_json_attr(row, "retrieval_configs", {})),
            metadata=load_json_attr(row, "metadata", {}),
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        return {
            "object": self.object_name(),
            "assistant_id": self.assistant_id,
            "model_id": self.model_id,
            "name": self.name,
            "description": self.description,
            "system_prompt_template": self.system_prompt_template,
            "memory": self.memory.model_dump(),
            "tools": self.tools,
            "retrievals": self.retrievals,
            "retrieval_configs": self.retrieval_configs.model_dump(),
            "metadata": self.metadata,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }

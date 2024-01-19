from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator, Extra
from ..utils import validate_metadata
from common.models import (
    AssistantMemory,
    build_assistant_memory,
    AssistantRetrievalConfig,
    AssistantRetrieval,
    AssistantTool,
)


# ----------------------------
# Create Assistant
# POST /assistants


class AssistantCreateRequest(BaseModel):
    model_id: str = Field(
        ...,
        min_length=8,
        max_length=8,
        description="The ID of an available chat completion model in your project.",
        examples=["abcdefgh"],
    )

    name: str = Field("", min_length=0, max_length=256, description="The assistant name", examples=["My Assistant"])

    description: str = Field(
        "", min_length=0, max_length=512, description="The assistant description", examples=["A helpful assistant"]
    )

    system_prompt_template: List[str] = Field(
        [],
        min_items=0,
        max_items=32,
        description="A list of system prompt chunks "
        "where prompt variables are wrapped by curly brackets, e.g. `{{variable}}`.",
        examples=[["You are a professional assistant speaking {{language}}."]],
    )

    memory: AssistantMemory = Field(..., description="The assistant memory.")

    tools: List[AssistantTool] = Field([], min_items=0, max_items=32, description="A list of tools.")

    retrievals: List[AssistantRetrieval] = Field(
        [], min_items=0, max_items=32, description="A list of retrieval sources."
    )

    retrieval_configs: AssistantRetrievalConfig = Field(AssistantRetrievalConfig(), description="Retrieval configs.")

    metadata: Dict[str, str] = Field(
        {},
        min_items=0,
        max_items=16,
        description="The assistant metadata. It can store up to 16 key-value pairs "
        "where each key's length is less than 64 and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("system_prompt_template", mode="before")
    def validate_system_prompt_template(cls, system_prompt_template):
        if system_prompt_template is None:
            return []

        # cast to list
        if isinstance(system_prompt_template, str):
            system_prompt_template = [system_prompt_template]

        # check total length
        total_length = sum([len(i) for i in system_prompt_template])
        if total_length > 16384:
            raise ValueError("The total prompt length should be less than 16384")

        return system_prompt_template

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        if not metadata:
            return {}
        return validate_metadata(metadata)

    @field_validator("tools")
    def validate_tools(cls, tools):
        # check all tools id are different
        tool_ids = [i.id for i in tools]
        if len(tool_ids) != len(set(tool_ids)):
            raise ValueError("All tool ids should be different.")
        return tools

    @field_validator("retrievals")
    def validate_retrievals(cls, retrievals):
        # check all retrievals id are different
        retrieval_ids = [i.id for i in retrievals]
        if len(retrieval_ids) != len(set(retrieval_ids)):
            raise ValueError("All retrieval ids should be different.")
        return retrievals

    @field_validator("memory", mode="before")
    def validate_memory(cls, memory_dict: Dict):
        memory: AssistantMemory = build_assistant_memory(memory_dict)
        if not memory:
            raise ValueError("Invalid input memory")
        return memory


# ----------------------------
# Update Assistant
# POST /assistants/{assistant_id}


class AssistantUpdateRequest(BaseModel):
    model_id: Optional[str] = Field(
        None,
        min_length=8,
        max_length=8,
        description="The ID of an available chat completion model in your project.",
        examples=["abcdefgh"],
    )

    name: Optional[str] = Field(
        None, min_length=0, max_length=256, description="The assistant name", examples=["My Assistant"]
    )

    description: Optional[str] = Field(
        None, min_length=0, max_length=512, description="The assistant description", examples=["A helpful assistant"]
    )

    system_prompt_template: Optional[List[str]] = Field(
        None,
        min_items=0,
        max_items=32,
        description="A list of system prompt chunks "
        "where prompt variables are wrapped by curly brackets, e.g. `{{variable}}`.",
        examples=[["You are a professional assistant speaking {{language}}."]],
    )

    memory: Optional[AssistantMemory] = Field(None, description="The assistant memory.")

    tools: Optional[List[AssistantTool]] = Field(None, min_items=0, max_items=32, description="A list of tools.")

    retrievals: Optional[List[AssistantRetrieval]] = Field(
        None, min_items=0, max_items=32, description="A list of retrieval sources."
    )

    retrieval_configs: Optional[AssistantRetrievalConfig] = Field(None, description="Retrieval configs.")

    metadata: Optional[Dict[str, str]] = Field(
        None,
        min_items=0,
        max_items=16,
        description="The assistant metadata. It can store up to 16 key-value pairs "
        "where each key's length is less than 64 and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("system_prompt_template", mode="before")
    def validate_system_prompt_template(cls, system_prompt_template):
        if system_prompt_template is None:
            return []

        # cast to list
        if isinstance(system_prompt_template, str):
            system_prompt_template = [system_prompt_template]

        # check total length
        total_length = sum([len(i) for i in system_prompt_template])
        if total_length > 16384:
            raise ValueError("The total prompt length should be less than 16384")

        return system_prompt_template

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        if not metadata:
            return {}
        return validate_metadata(metadata)

    @field_validator("tools")
    def validate_tools(cls, tools):
        # check all tools id are different
        tool_ids = [i.id for i in tools]
        if len(tool_ids) != len(set(tool_ids)):
            raise ValueError("All tool ids should be different.")
        return tools

    @field_validator("retrievals")
    def validate_retrievals(cls, retrievals):
        # check all retrievals id are different
        retrieval_ids = [i.id for i in retrievals]
        if len(retrieval_ids) != len(set(retrieval_ids)):
            raise ValueError("All retrieval ids should be different.")
        return retrievals

    @field_validator("memory", mode="before")
    def validate_memory(cls, memory_dict: Dict):
        memory: AssistantMemory = build_assistant_memory(memory_dict)
        if not memory:
            raise ValueError("Invalid input memory")
        return memory

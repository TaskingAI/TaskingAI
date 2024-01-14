from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

__all__ = [
    "AssistantRetrievalMethod",
    "AssistantRetrieval",
    "AssistantRetrievalConfig",
]


class AssistantRetrievalMethod(str, Enum):
    FUNCTION_CALL = "function_call"
    USER_MESSAGE = "user_message"
    MEMORY = "memory"


class AssistantRetrieval(BaseModel):
    type: str = Field(
        ..., description="The retrieval source type. Currently only `collection` is supported.", examples=["collection"]
    )
    id: str = Field(..., description="The retrieval source ID.", examples=["collection_1"])


class AssistantRetrievalConfig(BaseModel):
    top_k: int = Field(
        3,
        ge=1,
        le=20,
        description="Specifies the maximum number of relevant text chunks to retrieve during the "
        "retrieval-augmented generation process.",
        examples=[3],
    )
    max_tokens: Optional[int] = Field(
        None,
        ge=1,
        le=8192,
        description="Specifies the maximum token number of relevant text chunks to retrieve.",
        examples=[1000],
    )

    method: AssistantRetrievalMethod = Field(
        AssistantRetrievalMethod.MEMORY, description="The retrieval method.", examples=["function_call"]
    )

    function_description: Optional[str] = Field(
        None,
        description="Describes the purpose and appropriate context for triggering the retrieval function, "
        "guiding the assistant on when it is most useful to invoke it.",
        examples=[
            "Trigger this function to search TaskingAI's documentation "
            "for specific information about the product's features and applications."
        ],
    )

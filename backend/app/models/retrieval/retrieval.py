from typing import Dict
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

__all__ = ["RetrievalMethod", "RetrievalType", "RetrievalRef", "RetrievalConfig", "RetrievalResult"]


class RetrievalMethod(str, Enum):
    FUNCTION_CALL = "function_call"
    USER_MESSAGE = "user_message"
    MEMORY = "memory"


class RetrievalType(str, Enum):
    COLLECTION = "collection"


class RetrievalRef(BaseModel):
    type: RetrievalType = Field(
        ..., description="The retrieval source type. Currently only `collection` is supported.", examples=["collection"]
    )
    id: str = Field(..., description="The retrieval source ID.", examples=["collection_1"])


class RetrievalConfig(BaseModel):
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
        description="Specifies the maximum token number of relevant text chunks to retrieve.",
        examples=[1000],
    )

    score_threshold: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Specifies the minimum score threshold for relevant text chunks to retrieve.",
        examples=[0.5],
    )

    method: RetrievalMethod = Field(RetrievalMethod.MEMORY, description="The retrieval method.", examples=["memory"])

    function_description: Optional[str] = Field(
        None,
        description="Describes the purpose and appropriate context for triggering the retrieval function, "
        "guiding the assistant on when it is most useful to invoke it.",
        examples=[
            "Trigger this function to search TaskingAI's documentation "
            "for specific information about the product's features and applications."
        ],
    )


class RetrievalResult(BaseModel):
    ref: Dict = Field(
        ...,
        description="The reference of the retrieval output.",
        examples=[
            {
                "type": "collection",
                "collection_id": "collection_1",
                "chunk_id": "chunk_1",
            }
        ],
    )
    content: str = Field(
        ...,
        description="The content of the retrieval output.",
        examples=["Machine learning is ..."],
    )

from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator, Extra
from typing import Any, Dict
from ..utils import check_update_keys, validate_metadata

# ----------------------------
# Create Collection
# POST /collections


class CollectionCreateRequest(BaseModel):
    capacity: int = Field(
        1000,
        description="The collection capacity. "
        "Currently only 1000 is supported and we'll provide more options in the future.",
        examples=[1000],
    )
    embedding_model_id: str = Field(
        ...,
        min_length=8,
        max_length=8,
        description="The ID of an available text embedding model in your project.",
        examples=["abcdefgh"],
    )
    name: str = Field("", min_length=0, max_length=256, description="The collection name", example="My Collection")

    description: str = Field(
        "",
        min_length=0,
        max_length=512,
        description="The collection description",
        example="A collection of project documents.",
    )

    metadata: Dict[str, str] = Field(
        {},
        min_items=0,
        max_items=16,
        description="The collection metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        return validate_metadata(metadata)

    @field_validator("capacity")
    def validate_capacity(cls, capacity):
        if capacity not in [1000]:
            raise ValueError(
                "Currently only capacity of 1000 is supported " "and we will support more options in the future."
            )
        return capacity

    class Config:
        extra = Extra.forbid


# ----------------------------
# Update Collection
# POST /collections/{collection_id}
class CollectionUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None, min_length=0, max_length=256, description="The collection name", example="My Collection"
    )

    description: Optional[str] = Field(
        None,
        min_length=0,
        max_length=512,
        description="The collection description",
        example="A collection of project documents.",
    )

    metadata: Optional[Dict[str, str]] = Field(
        None,
        min_items=0,
        max_items=16,
        description="The collection metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        return validate_metadata(metadata)

    @model_validator(mode="before")
    def validate_all_fields_at_the_same_time(cls, data: Any):
        check_update_keys(data, ["name", "description", "metadata"])
        return data

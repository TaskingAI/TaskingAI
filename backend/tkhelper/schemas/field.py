from typing import Optional, Tuple
from pydantic import Field

__all__ = [
    "metadata_field",
    "created_timestamp_field",
    "updated_timestamp_field",
    "id_field",
    "name_field",
    "description_field",
]


def metadata_field() -> Field:
    return Field(
        {},
        min_length=0,
        max_length=16,
        description="The collection metadata. It can store up to 16 key-value pairs where each key's "
        "length is less than 64 and value's length is less than 512.",
        examples=[{"key1": "value1"}, {"key2": "value2"}],
    )


def created_timestamp_field() -> Field:
    return Field(
        ...,
        ge=0,
        description="The timestamp when the object was created in milliseconds.",
        examples=[1700000000000],
    )


def updated_timestamp_field() -> Field:
    return Field(
        ...,
        ge=0,
        description="The timestamp when the object was last updated in milliseconds.",
        examples=[1700000000000],
    )


def id_field(object_name: str, length: Optional[int] = None, length_range: Optional[Tuple[int, int]] = None) -> Field:
    if length:
        return Field(
            ...,
            min_length=length,
            max_length=length,
            description=f"The {object_name} ID.",
            pattern="^[a-zA-Z0-9]+$",
            examples=[f"{object_name}_id"],
        )
    elif length_range:
        return Field(
            ...,
            min_length=length_range[0],
            max_length=length_range[1],
            description=f"The {object_name} ID.",
            pattern="^[a-zA-Z0-9]+$",
            examples=[f"{object_name}_id"],
        )
    else:
        raise ValueError("Either length or length_range must be provided.")


def name_field(description: str = None) -> Field:
    return Field("", min_length=0, max_length=127, description=description or "The object's name.", examples=["Name"])


def description_field(description: str = None) -> Field:
    return Field(
        "",
        min_length=0,
        max_length=512,
        description=description or "The object's description.",
        examples=["Description"],
    )

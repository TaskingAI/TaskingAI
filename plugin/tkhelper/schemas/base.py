from typing import Any, Optional

from pydantic import BaseModel, Extra, Field
from tkhelper.models import SortOrderEnum


__all__ = [
    "BaseEmptyResponse",
    "BaseDataResponse",
    "BaseListResponse",
    "BaseListRequest",
]


class BaseEmptyResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The status of the response.")


class BaseDataResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The status of the response.")
    data: Any = Field(...)


class BaseListResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The status of the response.")
    data: Any = Field(..., description="The list of objects.")
    fetched_count: int = Field(0, description="The number of objects fetched.")
    total_count: Optional[int] = Field(None, description="The total number of objects.")
    has_more: bool = Field(False, description="Whether there are more objects to fetch.")


class BaseListRequest(BaseModel):
    limit: int = Field(
        20,
        ge=1,
        le=100,
        description="The maximum number of objects to return.",
        examples=[20],
    )

    # todo: add different sort field options
    order: Optional[SortOrderEnum] = Field(
        SortOrderEnum.DESC,
        description="The order of objects to return, `asc` for ascending and `desc` for descending.",
        examples=["desc"],
    )

    after: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="The cursor represented by a object_id to fetch the next page of objects.",
        examples=["object_id"],
    )

    before: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="The cursor represented by a object_id to fetch the previous page of objects.",
        examples=["object_id"],
    )

    equal_filter: Optional[str] = Field(
        "{}",
        description="A json string representing the equal filter.",
        examples=['{"type": "object_type_1"}'],
    )

    prefix_filter: Optional[str] = Field(
        "{}",
        description="A json string representing the prefix filter.",
        examples=['{"name": "name_prefix", "object_id": "object_id_prefix"}'],
    )

    class Config:
        extra = Extra.forbid

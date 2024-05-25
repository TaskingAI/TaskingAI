from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, model_validator
from tkhelper.models import SortOrderEnum
from .utils import validate_list_cursors


class BaseEmptyResponse(BaseModel):
    status: str = Field("success")


class BaseDataResponse(BaseModel):
    status: str = Field("success")
    data: Optional[Any] = None


class BaseErrorResponse(BaseModel):
    status: str = "error"
    error: Dict[str, Any]


class BaseListResponse(BaseModel):
    status: str = Field("success")
    data: Any
    fetched_count: int
    total_count: Optional[int] = Field(None)
    has_more: Optional[bool] = Field(None)


class BaseListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of objects to return.", examples=[20])

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
    )

    before: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="The cursor represented by a object_id to fetch the previous page of objects.",
    )

    offset: Optional[int] = Field(
        None,
        ge=0,
        description="The offset of objects to return. "
        "Only one in `offset`, `after` and `before` can be used at the same time.",
    )

    id_search: Optional[str] = Field(None, min_length=1, max_length=50, description="The object ID to search for.")

    name_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The object name to search for.")

    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        return validate_list_cursors(data)

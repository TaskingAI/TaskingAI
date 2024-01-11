from typing import Optional, Any, Dict
from pydantic import BaseModel, Field
from enum import Enum


class BaseSuccessEmptyResponse(BaseModel):
    status: str = Field("success")


class BaseSuccessDataResponse(BaseModel):
    status: str = Field("success")
    data: Optional[Any] = None


class BaseErrorResponse(BaseModel):
    status: str = "error"
    error: Dict[str, Any]


class BaseSuccessListTotalResponse(BaseModel):
    status: str = Field("success")
    data: Any
    fetched_count: int
    total_count: int


class BaseSuccessListHasMoreResponse(BaseModel):
    status: str = Field("success")
    data: Any
    fetched_count: int
    has_more: bool


class BaseSuccessFetchResponse(BaseModel):
    status: str = Field("success")
    data: Any
    fetched_count: int


class BaseSuccessListResultResponse(BaseModel):
    status: str
    results: Any
    success_count: int
    total_count: int


class SortOrderEnum(str, Enum):
    desc = "desc"
    asc = "asc"

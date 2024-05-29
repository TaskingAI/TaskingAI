from typing import Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

__all__ = [
    "BaseSuccessEmptyResponse",
    "BaseSuccessDataResponse",
    "BaseSuccessListResponse",
]


class BaseSuccessEmptyResponse(BaseModel):
    status: str = Field("success")


class BaseSuccessDataResponse(BaseModel):
    status: str = Field("success")
    data: Optional[Any] = None


class BaseSuccessListResponse(BaseModel):
    status: str = Field("success")
    data: Any
    fetched_count: int
    total_count: Optional[int] = Field(None)
    has_more: Optional[bool] = Field(None)


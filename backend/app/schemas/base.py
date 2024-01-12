from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class BaseSuccessEmptyResponse(BaseModel):
    status: str = Field("success")


class BaseSuccessDataResponse(BaseModel):
    status: str = Field("success")
    data: Optional[Any] = None


class BaseErrorResponse(BaseModel):
    status: str = "error"
    error: Dict[str, Any]


class BaseSuccessListResponse(BaseModel):
    status: str = Field("success")
    data: Any
    fetched_count: int
    total_count: Optional[int] = Field(None)
    has_more: Optional[bool] = Field(None)

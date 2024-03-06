from pydantic import BaseModel, Field
from typing import Dict, Optional

__all__ = [
    "ModelCreateRequest",
    "ModelUpdateRequest",
]


# POST /projects/{project_id}/models/create
class ModelCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    model_schema_id: str = Field(..., min_length=1, max_length=50)
    credentials: Dict = Field({})


# POST /projects/{project_id}/models/update
class ModelUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    credentials: Optional[Dict] = Field(default=None)

from pydantic import BaseModel, Field


__all__ = ["AdminLoginRequest"]

# ----------------------------
# Login Admin
# POST /admin/login


class AdminLoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(..., min_length=8, max_length=32)

from pydantic import BaseModel, Field


# ----------------------------
# Login Admin
# POST /admin/login


class AdminLoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(..., min_length=8, max_length=32)

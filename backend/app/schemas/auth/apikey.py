from pydantic import BaseModel, Field

__all__ = [
    "ApikeyGetRequest",
]

# ----------------------------
# Get API Key
# Get /apikeys/{apikey_id}


class ApikeyGetRequest(BaseModel):
    plain: bool = Field(False, description="Whether to return the API key in plain text.")

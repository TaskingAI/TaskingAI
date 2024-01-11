from pydantic import BaseModel, Field


# ----------------------------
# Create API Key
# POST /apikeys


class CreateApikeyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the API key.")


# ----------------------------
# Update API Key
# POST /apikeys/{apikey_id}


class UpdateApikeyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="API key name.")


# ----------------------------
# Get API Key
# Get /apikeys/{apikey_id}


class GetApikeyRequest(BaseModel):
    plain: bool = Field(False, description="Whether to return the API key in plain text.")

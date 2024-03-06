from typing import Dict, List

from pydantic import BaseModel, Field

from app.models import Plugin


class BundleInstanceCreateRequest(BaseModel):
    name: str = Field(
        "",
        description="The plugin bundle name.",
        max_length=127,
        examples=["My Bundle Instance"],
    )
    credentials: Dict = Field({})
    bundle_id: str = Field(...)
    max_count: int = Field(
        0,
        ge=0,
        description="The maximum number of plugin bundles allowed in a project.",
    )


class BundleInstanceUpdateRequest(BaseModel):
    name: str = Field(...)
    credentials: Dict = Field(...)


class BundleInstanceResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The response status.",
    )
    data: Dict = Field(..., description="The Bundle Instance API response data.")


class BundleListRequest(BaseModel):
    limit: int = Field(
        20,
        ge=1,
        le=100,
        description="The maximum number of model schemas to return.",
        examples=[20],
    )
    offset: int = Field(0, ge=0, description="The offset of model schemas to return. ")
    lang: str = Field(
        "en",
        min_length=1,
        max_length=50,
        description="The language code of the return data.",
        examples=["en"],
    )


class PluginListRequest(BaseModel):
    bundle_id: str = Field(default=None, min_length=1, max_length=50)
    lang: str = Field(
        "en",
        min_length=1,
        max_length=50,
        description="The language code of the return data.",
        examples=["en"],
    )


class PluginListResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The response status.",
        examples=["success"],
    )
    data: List[Plugin] = Field(..., description="The plugin API response data.")

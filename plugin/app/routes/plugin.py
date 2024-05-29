from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.cache import list_plugins

router = APIRouter()


class PluginListRequest(BaseModel):

    bundle_id: Optional[str] = Field(
        None,
        description="The bundle id.",
        examples=["bundle_id_1", "bundle_id_2"],
    )

    lang: str = Field(
        "en",
        description="The language code of the response.",
        examples=["en", "zh", "fr"],
    )


class PluginListResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )
    data: List[Dict] = Field(
        ...,
        description="The list of Plugins.",
        # todo: add examples
    )


@router.get(
    "/plugins",
    summary="List plugins",
    operation_id="list_plugins",
    response_model=PluginListResponse,
    tags=["Plugin"],
    responses={422: {"description": "Unprocessable Entity"}},
)
async def api_list_plugins(
    request: Request,
    data: PluginListRequest = Depends(),
):
    plugins = list_plugins(data.bundle_id)
    return PluginListResponse(
        status="success",
        data=[p.to_dict(data.lang) for p in plugins],
    )

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Dict
from app.cache import list_bundles

router = APIRouter()


class BundleListRequest(BaseModel):

    lang: str = Field(
        "en",
        description="The language code of the response.",
        examples=["en"],
    )


class BundleListResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )
    data: List[Dict] = Field(
        ...,
        description="The list of bundles.",
    )


@router.get(
    "/bundles",
    summary="List bundles",
    operation_id="list_bundles",
    response_model=BundleListResponse,
    tags=["Plugin"],
    responses={422: {"description": "Unprocessable Entity"}},
)
async def api_list_providers(
    request: Request,
    data: BundleListRequest = Depends(),
):
    bundles = list_bundles()
    return BundleListResponse(
        status="success",
        data=[p.to_dict(data.lang) for p in bundles],
    )

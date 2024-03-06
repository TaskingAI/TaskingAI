from fastapi import APIRouter, Depends, Request
from tkhelper.schemas import BaseDataResponse, BaseListResponse

from app.schemas.tool import *
from app.services.tool import *

from ..utils import auth_info_required

router = APIRouter()


@router.get(
    "/bundles",
    tags=["Tool - Plugin"],
    summary="List Bundles",
    operation_id="list_bundles",
    response_model=BaseListResponse,
)
async def api_list_bundles(
    request: Request,
    data: BundleListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    bundles, total, has_more = list_bundles(
        limit=data.limit,
        offset=data.offset,
    )

    bundle_registered_dict = await get_bundle_registered_dict(
        bundle_ids=[bundle.bundle_id for bundle in bundles],
    )

    results = []
    for bundle in bundles:
        plugins = list_plugins(bundle.bundle_id)
        result = bundle.to_dict(data.lang)
        result["registered"] = bundle_registered_dict.get(bundle.bundle_id, False)
        result["plugins"] = [plugin.to_dict(data.lang) for plugin in plugins]
        results.append(result)

    return BaseListResponse(
        data=results,
        fetched_count=len(bundles),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/plugins",
    tags=["Tool - Plugin"],
    summary="List Plugins",
    operation_id="list_plugins",
    response_model=BaseDataResponse,
)
async def api_list_plugins(
    request: Request,
    data: PluginListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    plugins = list_plugins(data.bundle_id)

    return BaseListResponse(
        data=[plugin.to_dict(data.lang) for plugin in plugins],
        fetched_count=len(plugins),
        total_count=len(plugins),
        has_more=False,
    )

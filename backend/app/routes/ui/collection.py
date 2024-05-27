from typing import Dict

from fastapi import APIRouter, Depends, Request

from app.operators import collection_ops as ops
from app.routes.utils import (
    auth_info_required,
    check_path_params,
    path_params_required,
    validate_list_filter,
)
from app.schemas import CollectionListRequest
from tkhelper.schemas.base import BaseDataResponse, BaseListResponse

router = APIRouter()


@router.get(
    path="/ui/collections/{collection_id}",
    tags=["UI"],
    summary="Get UI Collection",
    operation_id="get_ui_collection",
)
async def api_get_ui_collection(
    request: Request,
    path_params: Dict = Depends(path_params_required),
    auth_info: Dict = Depends(auth_info_required),
):
    check_path_params(
        model_operator=ops,
        object_id_required=True,
        path_params=path_params,
    )

    data = await ops.ui_get(**path_params)
    return BaseDataResponse(data=data)


@router.get(
    path="/ui/collections",
    tags=["UI"],
    summary="List UI Collections",
    operation_id="list_ui_collection",
)
async def api_list_ui_collections(
    request: Request,
    data: CollectionListRequest = Depends(),
    path_params: Dict = Depends(path_params_required),
    auth_info: Dict = Depends(auth_info_required),
):
    check_path_params(
        model_operator=ops,
        object_id_required=False,
        path_params=path_params,
    )

    data_prefix_filter = getattr(data, "prefix_filter", "")
    data_equal_filter = getattr(data, "equal_filter", "")
    prefix_filter_dict, equal_filter_dict = await validate_list_filter(
        model_operator=ops,
        path_params=path_params,
        prefix_filter=data_prefix_filter,
        equal_filter=data_equal_filter,
    )

    data, has_more = await ops.ui_list(
        limit=data.limit,
        order=data.order,
        after_id=data.after,
        before_id=data.before,
        prefix_filters=prefix_filter_dict,
        equal_filters=equal_filter_dict,
        **path_params,
    )
    return BaseListResponse(
        data=data,
        fetched_count=len(data),
        has_more=has_more,
    )

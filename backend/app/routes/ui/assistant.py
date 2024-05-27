from typing import Dict

from fastapi import APIRouter, Depends, Request

from app.operators import assistant_ops as ops
from app.routes.utils import (
    auth_info_required,
    check_path_params,
    path_params_required,
    validate_list_filter,
)
from app.schemas import AssistantListRequest
from app.services.retrieval.retrieval import ui_fetch_retrievals
from app.services.tool.tool import ui_fetch_tools
from tkhelper.schemas.base import BaseDataResponse, BaseListResponse

router = APIRouter()


@router.get(
    path="/ui/assistants/{assistant_id}",
    tags=["UI"],
    summary="Get UI Assistant",
    operation_id="get_ui_assistant",
)
async def api_ui_get_assistant(
    request: Request,
    path_params: Dict = Depends(path_params_required),
    auth_info: Dict = Depends(auth_info_required),
):
    check_path_params(
        model_operator=ops,
        object_id_required=True,
        path_params=path_params,
    )

    assistant = await ops.ui_get(**path_params)
    assistant["tools"] = await ui_fetch_tools(assistant["tools"])
    assistant["retrievals"] = await ui_fetch_retrievals(assistant["retrievals"])
    return BaseDataResponse(data=assistant)


@router.get(
    path="/ui/assistants",
    tags=["UI"],
    summary="List UI Assistants",
    operation_id="list_ui_assistant",
)
async def api_ui_list_assistants(
    request: Request,
    data: AssistantListRequest = Depends(),
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
    for d in data:
        d["tools"] = await ui_fetch_tools(d["tools"])
        d["retrievals"] = await ui_fetch_retrievals(d["retrievals"])
    return BaseListResponse(
        data=data,
        fetched_count=len(data),
        has_more=has_more,
    )

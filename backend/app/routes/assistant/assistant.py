from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.database.postgres.pool import postgres_db_pool
from common.services.assistant.assistant import *
from app.schemas.assistant.assistant import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse, BaseListRequest
from common.models import Assistant, SerializePurpose

router = APIRouter()


@router.get(
    "/assistants",
    tags=["Assistant"],
    summary="List Assistants",
    operation_id="list_assistants",
    response_model=BaseSuccessListResponse,
)
async def api_list_assistants(
    request: Request,
    data: BaseListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    assistants, total, has_more = await list_assistants(
        postgres_conn,
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
        offset=data.offset,
        id_search=data.id_search,
        name_search=data.name_search,
    )
    return BaseSuccessListResponse(
        data=[assistant.to_dict(purpose=SerializePurpose.RESPONSE) for assistant in assistants],
        fetched_count=len(assistants),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/assistants/{assistant_id}",
    tags=["Assistant"],
    summary="Get Assistant",
    operation_id="get_assistant",
    response_model=BaseSuccessDataResponse,
)
async def api_get_assistant(
    assistant_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    assistant: Assistant = await get_assistant(
        postgres_conn=postgres_conn,
        assistant_id=assistant_id,
    )
    return BaseSuccessDataResponse(data=assistant.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/assistants",
    tags=["Assistant"],
    summary="Bulk create assistant",
    operation_id="bulk_create_assistant",
    response_model=BaseSuccessDataResponse,
)
async def api_create_assistants(
    request: Request,
    data: AssistantCreateRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    assistant: Assistant = await create_assistant(
        postgres_conn=postgres_conn,
        model_id=data.model_id,
        name=data.name,
        description=data.description,
        system_prompt_template=data.system_prompt_template,
        memory=data.memory,
        tools=data.tools,
        retrievals=data.retrievals,
        retrieval_configs=data.retrieval_configs,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(
        data=assistant.to_dict(
            purpose=SerializePurpose.RESPONSE,
        )
    )


@router.post(
    "/assistants/{assistant_id}",
    tags=["Assistant"],
    summary="Update Assistant",
    operation_id="update_assistant",
    response_model=BaseSuccessDataResponse,
)
async def api_update_assistant(
    assistant_id: str,
    request: Request,
    data: AssistantUpdateRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    assistant: Assistant = await update_assistant(
        postgres_conn=postgres_conn,
        assistant_id=assistant_id,
        model_id=data.model_id,
        name=data.name,
        description=data.description,
        system_prompt_template=data.system_prompt_template,
        memory=data.memory,
        tools=data.tools,
        retrievals=data.retrievals,
        retrieval_configs=data.retrieval_configs,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(data=assistant.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/assistants/{assistant_id}",
    tags=["Assistant"],
    summary="Delete Assistant",
    operation_id="delete_assistant",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_assistant(
    assistant_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    await delete_assistant(
        postgres_conn=postgres_conn,
        assistant_id=assistant_id,
    )
    return BaseSuccessEmptyResponse()

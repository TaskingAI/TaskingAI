from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.database.postgres.pool import postgres_db_pool
from common.services.retrieval.record import *
from app.schemas.retrieval.record import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse
from common.models import Record, SerializePurpose

router = APIRouter()


@router.get(
    "/collections/{collection_id}/records",
    tags=["Retrieval"],
    summary="List Records",
    operation_id="list_records",
    response_model=BaseSuccessListResponse,
)
async def api_list_records(
    request: Request,
    collection_id: str,
    data: RecordListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    records, total, has_more = await list_records(
        postgres_conn,
        collection_id=collection_id,
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
        offset=data.offset,
        id_search=data.id_search,
    )
    return BaseSuccessListResponse(
        data=[record.to_dict(purpose=SerializePurpose.RESPONSE) for record in records],
        fetched_count=len(records),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/collections/{collection_id}/records/{record_id}",
    tags=["Retrieval"],
    summary="Get Record",
    operation_id="get_record",
    response_model=BaseSuccessDataResponse,
)
async def api_get_record(
    record_id: str,
    request: Request,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    record: Record = await get_record(
        postgres_conn=postgres_conn,
        collection_id=collection_id,
        record_id=record_id,
    )
    return BaseSuccessDataResponse(data=record.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/collections/{collection_id}/records",
    tags=["Retrieval"],
    summary="Bulk create record",
    operation_id="bulk_create_record",
    response_model=BaseSuccessDataResponse,
)
async def api_create_records(
    request: Request,
    data: RecordCreateRequest,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    record: Record = await create_record(
        postgres_conn=postgres_conn,
        collection_id=collection_id,
        title=data.title,
        type=data.type,
        content=data.content,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(
        data=record.to_dict(
            purpose=SerializePurpose.RESPONSE,
        )
    )


@router.post(
    "/collections/{collection_id}/records/{record_id}",
    tags=["Retrieval"],
    summary="Update Record",
    operation_id="update_record",
    response_model=BaseSuccessDataResponse,
)
async def api_update_record(
    record_id: str,
    request: Request,
    data: RecordUpdateRequest,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    record: Record = await update_record(
        postgres_conn=postgres_conn,
        collection_id=collection_id,
        record_id=record_id,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(data=record.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/collections/{collection_id}/records/{record_id}",
    tags=["Record"],
    summary="Delete Record",
    operation_id="delete_record",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_record(
    record_id: str,
    request: Request,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    await delete_record(
        postgres_conn=postgres_conn,
        collection_id=collection_id,
        record_id=record_id,
    )
    return BaseSuccessEmptyResponse()

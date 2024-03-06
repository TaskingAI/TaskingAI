from fastapi import APIRouter, Depends, Request
from typing import Dict

from app.schemas.retrieval.record import *
from tkhelper.schemas.base import BaseEmptyResponse, BaseDataResponse
from app.models import Record
from app.services.retrieval import create_record, update_record, delete_record

from ..utils import auth_info_required

router = APIRouter()


@router.post(
    "/collections/{collection_id}/records",
    tags=["Retrieval"],
    summary="Create record",
    operation_id="create_record",
    response_model=BaseDataResponse,
)
async def api_create_records(
    request: Request,
    data: RecordCreateRequest,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    record: Record = await create_record(
        collection_id=collection_id,
        title=data.title,
        type=data.type,
        content=data.content,
        text_splitter=data.text_splitter,
        metadata=data.metadata,
    )
    return BaseDataResponse(data=record.to_response_dict())


@router.post(
    "/collections/{collection_id}/records/{record_id}",
    tags=["Retrieval"],
    summary="Update Record",
    operation_id="update_record",
    response_model=BaseDataResponse,
)
async def api_update_record(
    record_id: str,
    request: Request,
    data: RecordUpdateRequest,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    record: Record = await update_record(
        collection_id=collection_id,
        record_id=record_id,
        title=data.title,
        type=data.type,
        content=data.content,
        text_splitter=data.text_splitter,
        metadata=data.metadata,
    )
    return BaseDataResponse(data=record.to_response_dict())


@router.delete(
    "/collections/{collection_id}/records/{record_id}",
    tags=["Retrieval"],
    summary="Delete Record",
    operation_id="delete_record",
    response_model=BaseEmptyResponse,
)
async def api_delete_record(
    record_id: str,
    request: Request,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    await delete_record(
        collection_id=collection_id,
        record_id=record_id,
    )
    return BaseEmptyResponse()

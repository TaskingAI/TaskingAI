from ..utils import auth_info_required
from fastapi import APIRouter, Request, Depends
from common.services.retrieval.chunk import *
from app.schemas.retrieval.chunk import *
from app.schemas.base import BaseSuccessListResponse, BaseListRequest, BaseSuccessDataResponse, BaseSuccessEmptyResponse
from common.models import Chunk, SerializePurpose
from typing import List

router = APIRouter()


@router.post(
    "/collections/{collection_id}/chunks/query",
    tags=["Retrieval"],
    summary="Query chunks",
    operation_id="query_chunks",
    response_model=BaseSuccessListResponse,
)
async def api_query_chunk(
    request: Request,
    data: ChunkQueryRequest,
    collection_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    chunks: List[Chunk] = await query_chunks(
        collection_ids=[collection_id],
        top_k=data.top_k,
        query_text=data.query_text,
    )
    return BaseSuccessListResponse(
        data=[chunk.to_dict(purpose=SerializePurpose.RESPONSE) for chunk in chunks],
        fetched_count=len(chunks),
    ).model_dump(exclude_none=True)


@router.get(
    "/collections/{collection_id}/chunks",
    tags=["Retrieval"],
    summary="List Collection Chunks",
    operation_id="list_collection_chunks",
    response_model=BaseSuccessListResponse,
)
async def api_list_collection_chunks(
    request: Request,
    collection_id: str,
    data: BaseListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    records, total, has_more = await list_collection_chunks(
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
    "/collections/{collection_id}/records/{record_id}/chunks",
    tags=["Retrieval"],
    summary="List Record Chunks",
    operation_id="list_record_chunks",
    response_model=BaseSuccessListResponse,
)
async def api_list_record_chunks(
    request: Request,
    collection_id: str,
    record_id: str,
    data: BaseListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    records, total, has_more = await list_record_chunks(
        collection_id=collection_id,
        record_id=record_id,
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
    "/collections/{collection_id}/chunks/{chunk_id}",
    tags=["Retrieval"],
    summary="Get Chunk",
    operation_id="get_chunk",
    response_model=BaseSuccessDataResponse,
)
async def api_get_chunk(
    request: Request,
    collection_id: str,
    chunk_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    chunk: Chunk = await get_chunk(
        collection_id=collection_id,
        chunk_id=chunk_id,
    )
    return BaseSuccessDataResponse(data=chunk.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/collections/{collection_id}/chunks",
    tags=["Retrieval"],
    summary="Create chunk",
    operation_id="create_chunk",
    response_model=BaseSuccessDataResponse,
)
async def api_create_chunk(
    request: Request,
    collection_id: str,
    data: ChunkCreateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    chunk: Chunk = await create_chunk(
        collection_id=collection_id,
        content=data.content,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(data=chunk.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/collections/{collection_id}/chunks/{chunk_id}",
    tags=["Retrieval"],
    summary="Delete chunk",
    operation_id="delete_chunk",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_chunk(
    request: Request,
    collection_id: str,
    chunk_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    await delete_chunk(
        collection_id=collection_id,
        chunk_id=chunk_id,
    )
    return BaseSuccessEmptyResponse()


@router.post(
    "/collections/{collection_id}/chunks/{chunk_id}",
    tags=["Retrieval"],
    summary="Update chunk",
    operation_id="update_chunk",
    response_model=BaseSuccessDataResponse,
)
async def api_update_chunk(
    request: Request,
    collection_id: str,
    chunk_id: str,
    data: ChunkUpdateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    chunk: Chunk = await update_chunk(
        collection_id=collection_id,
        chunk_id=chunk_id,
        content=data.content,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(data=chunk.to_dict(purpose=SerializePurpose.RESPONSE))

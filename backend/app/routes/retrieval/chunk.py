from typing import List, Dict
from fastapi import APIRouter, Request, Depends

from app.schemas import *
from tkhelper.schemas.base import BaseListResponse, BaseListRequest, BaseDataResponse, BaseEmptyResponse
from app.models import Chunk
from app.services.retrieval import query_chunks, create_chunk, update_chunk, delete_chunk, list_record_chunks

from ..utils import auth_info_required

router = APIRouter()


@router.post(
    "/collections/{collection_id}/chunks/query",
    tags=["Retrieval"],
    summary="Query chunks",
    operation_id="query_chunks",
    response_model=BaseListResponse,
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
    return BaseListResponse(
        data=[chunk.to_response_dict() for chunk in chunks],
        fetched_count=len(chunks),
    ).model_dump(exclude_none=True)


@router.get(
    "/collections/{collection_id}/records/{record_id}/chunks",
    tags=["Retrieval"],
    summary="List Record Chunks",
    operation_id="list_record_chunks",
    response_model=BaseListResponse,
)
async def api_list_record_chunks(
    request: Request,
    collection_id: str,
    record_id: str,
    data: BaseListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    chunks, has_more = await list_record_chunks(
        collection_id=collection_id,
        record_id=record_id,
        limit=data.limit,
        order=data.order,
        after_id=data.after,
        before_id=data.before,
        prefix_filters=data.prefix_filters,
    )
    return BaseListResponse(
        data=[chunk.to_response_dict() for chunk in chunks],
        fetched_count=len(chunks),
        has_more=has_more,
    )


@router.post(
    "/collections/{collection_id}/chunks",
    tags=["Retrieval"],
    summary="Create chunk",
    operation_id="create_chunk",
    response_model=BaseDataResponse,
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
    return BaseDataResponse(data=chunk.to_response_dict())


@router.delete(
    "/collections/{collection_id}/chunks/{chunk_id}",
    tags=["Retrieval"],
    summary="Delete chunk",
    operation_id="delete_chunk",
    response_model=BaseEmptyResponse,
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
    return BaseEmptyResponse()


@router.post(
    "/collections/{collection_id}/chunks/{chunk_id}",
    tags=["Retrieval"],
    summary="Update chunk",
    operation_id="update_chunk",
    response_model=BaseDataResponse,
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
    return BaseDataResponse(data=chunk.to_response_dict())

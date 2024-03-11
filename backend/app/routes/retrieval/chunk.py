from typing import List, Dict
from fastapi import APIRouter, Request, Depends

from app.schemas import *
from tkhelper.schemas.base import BaseListResponse, BaseListRequest
from app.models import Chunk
from app.services.retrieval import query_chunks
from app.operators import chunk_ops
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
    chunks, has_more = await chunk_ops.list(
        collection_id=collection_id,
        limit=data.limit,
        order=data.order,
        after_id=data.after_id,
        before_id=data.before_id,
        prefix_filters=data.prefix_filters,
        equal_filters={"record_id": record_id},
    )

    return BaseListResponse(
        data=[chunk.to_response_dict() for chunk in chunks],
        fetched_count=len(chunks),
        has_more=has_more,
    )

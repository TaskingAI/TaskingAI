from fastapi import APIRouter
from common.services.retrieval.chunk import *
from app.schemas.retrieval.chunk import *
from app.schemas.base import BaseSuccessListResponse
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
async def api_query_chunk(data: ChunkQueryRequest, collection_id: str):
    chunks: List[Chunk] = await query_chunks(
        collection_ids=[collection_id],
        top_k=data.top_k,
        query_text=data.query_text,
    )
    return BaseSuccessListResponse(
        data=[chunk.to_dict(purpose=SerializePurpose.RESPONSE) for chunk in chunks],
        fetched_count=len(chunks),
    ).model_dump(exclude_none=True)


# todo: get, list, create, update, delete chunk

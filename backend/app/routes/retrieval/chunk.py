from fastapi import APIRouter, Depends
from common.database.postgres.pool import postgres_db_pool
from common.services.retrieval.chunk import *
from app.schemas.retrieval.chunk import *
from app.schemas.base import BaseSuccessListResponse
from common.models import Chunk, SerializePurpose
from typing import List

router = APIRouter()


@router.post(
    "/collections/{collection_id}/chunks/query",
)
async def api_query_chunk(
    data: ChunkQueryRequest, collection_id: str, postgres_conn=Depends(postgres_db_pool.get_db_connection)
):
    chunks: List[Chunk] = await query_chunks(
        postgres_conn,
        collection_ids=[collection_id],
        top_k=data.top_k,
        query_text=data.query_text,
    )
    return BaseSuccessListResponse(
        data=[chunk.to_dict(purpose=SerializePurpose.RESPONSE) for chunk in chunks],
        fetched_count=len(chunks),
    ).model_dump(exclude_none=True)


# todo: get, list, create, update, delete chunk

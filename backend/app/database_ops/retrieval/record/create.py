from app.database.connection import postgres_pool
from app.models import Collection, RecordType
from tkhelper.models import Status
from typing import Dict, List
import json
from .utils import insert_record_chunks


async def create_record_and_chunks(
    record_id: str,
    collection: Collection,
    chunk_text_list: List[str],
    chunk_embedding_list: List[List[float]],
    chunk_num_tokens_list: List[int],
    title: str,
    type: RecordType,
    content: str,
    metadata: Dict[str, str],
) -> None:
    """
    Create record and its chunks
    :param record_id: the record id
    :param collection: the collection where the record belongs to
    :param chunk_text_list: the text list of the chunks to be created
    :param chunk_embedding_list: the embedding list of the chunks to be created
    :param chunk_num_tokens_list: the num_tokens list of the chunks to be created
    :param title: the record title
    :param type: the record type
    :param content: the record content
    :param metadata: the record metadata
    :return: None
    """

    # generate record id

    async with postgres_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert record into database
            await conn.execute(
                """
                INSERT INTO record (record_id, collection_id, title, type, content, status, metadata, num_chunks)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
                record_id,
                collection.collection_id,
                title,
                type.value,
                content,
                Status.READY.value,
                json.dumps(metadata),
                len(chunk_text_list),
            )

            # 2. insert chunks
            await insert_record_chunks(
                conn=conn,
                collection_id=collection.collection_id,
                record_id=record_id,
                chunk_text_list=chunk_text_list,
                chunk_embedding_list=chunk_embedding_list,
                chunk_num_tokens_list=chunk_num_tokens_list,
            )

            # 3. update collection stats
            await conn.execute(
                """
                UPDATE collection
                SET num_records = num_records + 1,
                    num_chunks = num_chunks + $1
                WHERE collection_id = $2
            """,
                len(chunk_text_list),
                collection.collection_id,
            )

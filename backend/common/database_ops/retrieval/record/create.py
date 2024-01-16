from common.database.postgres.pool import postgres_db_pool
from common.models import Collection, Record, RecordType, Status
from .get import get_record
from typing import Dict, List
import json
from .utils import insert_record_chunks


async def create_record_and_chunks(
    collection: Collection,
    chunk_texts: List[str],
    chunk_embeddings: List[List[float]],
    title: str,
    type: RecordType,
    content: str,
    metadata: Dict[str, str],
) -> Record:
    """
    Create record and its chunks
    :param collection: the collection where the record belongs to
    :param chunk_texts: the text list of the chunks to be created
    :param chunk_embeddings: the embedding list of the chunks to be created
    :param title: the record title
    :param type: the record type
    :param content: the record content
    :param metadata: the record metadata
    :return: the created record
    """

    # generate record id
    new_record_id = Record.generate_random_id()

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert record into database
            await conn.execute(
                """
                INSERT INTO record (record_id, collection_id, title, type, content, status, metadata, num_chunks)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
                new_record_id,
                collection.collection_id,
                title,
                type.value,
                content,
                Status.READY.value,
                json.dumps(metadata),
                len(chunk_texts),
            )

            # 2. insert chunks
            await insert_record_chunks(
                conn=conn,
                collection_id=collection.collection_id,
                record_id=new_record_id,
                chunk_texts=chunk_texts,
                chunk_embeddings=chunk_embeddings,
            )

            # 3. update collection stats
            await conn.execute(
                """
                UPDATE collection
                SET num_records = num_records + 1,
                    num_chunks = num_chunks + $1
                WHERE collection_id = $2
            """,
                len(chunk_texts),
                collection.collection_id,
            )

            await collection.pop_redis()

    # 4. get and return
    record = await get_record(collection=collection, record_id=new_record_id)

    return record

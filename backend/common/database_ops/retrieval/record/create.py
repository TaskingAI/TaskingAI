from common.database.postgres.pool import postgres_db_pool
from common.models import Collection, Record, Chunk, RecordType, Status
from .get import get_record
from typing import Dict, List
import json


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

    # prepare chunk insert sql
    num_chunks = len(chunk_texts)
    chunk_table_name = Collection.get_chunk_table_name(collection.collection_id)

    insert_values_sql = ", ".join(
        [
            f"(${i * 6 + 1}, ${i * 6 + 2}, ${i * 6 + 3}, ${i * 6 + 4}, ${i * 6 + 5}, ${i * 6 + 6})"
            for i in range(num_chunks)
        ]
    )

    #  prepare chunk insert params
    params = []
    for i in range(num_chunks):
        new_chunk_id = Chunk.generate_random_id()
        params.extend(
            [
                new_chunk_id,
                new_record_id,
                collection.collection_id,
                json.dumps(chunk_embeddings[i]),
                chunk_texts[i],
                "{}",
            ]
        )

    # make the final insert sql
    insert_chunks_sql = f"""
        INSERT INTO {chunk_table_name}(chunk_id, record_id, collection_id, embedding, content, metadata)
        VALUES {insert_values_sql};
    """

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

            await conn.execute(insert_chunks_sql, *params)

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

    # 4. get and return
    record = await get_record(collection=collection, record_id=new_record_id)

    return record

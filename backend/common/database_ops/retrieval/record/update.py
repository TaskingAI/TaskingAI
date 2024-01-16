from common.database.postgres.pool import postgres_db_pool
from common.models import Record, Collection, RecordType
from typing import Dict, Optional, List
from common.database_ops.utils import update_object
from .get import get_record
from .utils import insert_record_chunks, delete_record_chunks


async def update_record(
    collection: Collection,
    record: Record,
    title: Optional[str],
    type: Optional[RecordType],
    chunk_texts: Optional[List[str]],
    chunk_embeddings: Optional[List[List[float]]],
    metadata: Optional[Dict],
):
    # build update dict
    update_dict = {}
    if title is not None:
        update_dict["title"] = title
    if type is not None:
        update_dict["type"] = type.value
    if metadata is not None:
        update_dict["metadata"] = metadata

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            if chunk_texts is not None and chunk_embeddings is not None:
                # 1. delete old chunks
                await delete_record_chunks(
                    conn=conn,
                    collection_id=collection.collection_id,
                    record_id=record.record_id,
                )

                # 2. insert new chunks
                await insert_record_chunks(
                    conn=conn,
                    collection_id=collection.collection_id,
                    record_id=record.record_id,
                    chunk_texts=chunk_texts,
                    chunk_embeddings=chunk_embeddings,
                )

                # 3. update record num_chunks
                update_dict["num_chunks"] = len(chunk_texts)

                # 4. update collection num_chunks
                await update_object(
                    conn,
                    update_dict={"num_chunks": collection.num_chunks - record.num_chunks + len(chunk_texts)},
                    update_time=True,
                    table_name="collection",
                    equal_filters={"collection_id": collection.collection_id},
                )
                await collection.pop_redis()

            # 5. update other chunk fields
            if len(update_dict) > 0:
                await update_object(
                    conn,
                    update_dict=update_dict,
                    update_time=True,
                    table_name="record",
                    equal_filters={"record_id": record.record_id},
                )

    # 6. Get updated record
    record = await get_record(collection, record.record_id)

    return record

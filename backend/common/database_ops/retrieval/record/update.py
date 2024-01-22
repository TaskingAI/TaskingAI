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
    content: Optional[str],
    chunk_text_list: Optional[List[str]],
    chunk_embedding_list: Optional[List[List[float]]],
    chunk_num_tokens_list: Optional[List[int]],
    metadata: Optional[Dict],
):
    """
    Update record

    :param collection: the collection where the record belongs to
    :param record: the record to be updated
    :param title: the record title
    :param type: the record type
    :param content: the record content
    :param chunk_text_list: the text list of the chunks to be updated
    :param chunk_embedding_list: the embedding list of the chunks to be updated
    :param chunk_num_tokens_list: the num_tokens list of the chunks to be updated
    :param metadata: the record metadata
    :return: the updated record
    """

    # build update dict
    update_dict = {}
    if title is not None:
        update_dict["title"] = title
    if type is not None:
        update_dict["type"] = type.value
    if metadata is not None:
        update_dict["metadata"] = metadata
    if content is not None:
        update_dict["content"] = content

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            if chunk_text_list is not None and chunk_embedding_list is not None:
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
                    chunk_text_list=chunk_text_list,
                    chunk_embedding_list=chunk_embedding_list,
                    chunk_num_tokens_list=chunk_num_tokens_list,
                )

                # 3. update record num_chunks
                update_dict["num_chunks"] = len(chunk_text_list)

                # 4. update collection num_chunks
                await update_object(
                    conn,
                    update_dict={"num_chunks": collection.num_chunks - record.num_chunks + len(chunk_text_list)},
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

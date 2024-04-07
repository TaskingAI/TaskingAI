from typing import List
from app.models import Collection, Chunk
import json
from tkhelper.utils import current_timestamp_int_milliseconds


async def insert_record_chunks(
    conn,
    collection_id: str,
    record_id: str,
    chunk_text_list: List[str],
    chunk_embedding_list: List[List[float]],
    chunk_num_tokens_list: List[int],
):
    """
    Insert record chunks
    :param conn:
    :param collection_id: the collection id
    :param record_id: the record id
    :param chunk_text_list: the text list of the chunks to be created
    :param chunk_embedding_list: the embedding list of the chunks to be created
    :param chunk_num_tokens_list: the num_tokens list of the chunks to be created
    :return:
    """

    # prepare chunk insert sql
    num_chunks = len(chunk_text_list)
    chunk_table_name = Collection.get_chunk_table_name(collection_id)

    # make different timestamps for each chunk
    current_timestamp = current_timestamp_int_milliseconds()
    timestamps = [current_timestamp + i for i in range(len(chunk_text_list))]

    insert_values_sql = ", ".join(
        [
            f"("
            f"${i * 9 + 1}, "
            f"${i * 9 + 2}, "
            f"${i * 9 + 3}, "
            f"${i * 9 + 4}, "
            f"${i * 9 + 5}, "
            f"${i * 9 + 6}, "
            f"${i * 9 + 7}, "
            f"${i * 9 + 8}, "
            f"${i * 9 + 9}"
            f")"
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
                record_id,
                collection_id,
                json.dumps(chunk_embedding_list[i]),
                chunk_text_list[i],
                "{}",
                timestamps[i],
                timestamps[i],
                chunk_num_tokens_list[i],
            ]
        )

    # make the final insert sql
    insert_chunks_sql = f"""
        INSERT INTO {chunk_table_name}(chunk_id, record_id, collection_id, embedding, content,
         metadata, updated_timestamp, created_timestamp, num_tokens)
        VALUES {insert_values_sql};
    """

    # insert chunks
    await conn.execute(insert_chunks_sql, *params)


async def delete_record_chunks(conn, collection_id: str, record_id: str) -> int:
    """
    Delete record chunks
    :param conn:
    :param collection_id: the collection id
    :param record_id: the record id
    :return: the content_bytes sum of chunks, and the number of chunks
    """

    chunk_table_name = Collection.get_chunk_table_name(collection_id)

    # count chunks and the content_bytes sum of chunks
    result = await conn.fetchrow(
        f"""
        SELECT COUNT(*)
        FROM {chunk_table_name}
        WHERE record_id = $1
    """,
        record_id,
    )
    num_chunks = result[0] or 0

    await conn.execute(
        f"""
        DELETE FROM {chunk_table_name}
        WHERE record_id = $1
    """,
        record_id,
    )

    return num_chunks

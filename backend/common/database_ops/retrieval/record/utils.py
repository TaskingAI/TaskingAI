from typing import List
from common.models import Collection, Chunk
import json
from common.utils import current_timestamp_int_milliseconds


async def insert_record_chunks(
    conn,
    collection_id: str,
    record_id: str,
    chunk_texts: List[str],
    chunk_embeddings: List[List[float]],
):
    """
    Insert record chunks
    :param conn:
    :param collection_id: the collection id
    :param record_id: the record id
    :param chunk_texts: the text list of the chunks to be created
    :param chunk_embeddings: the embedding list of the chunks to be created
    :return:
    """

    # prepare chunk insert sql
    num_chunks = len(chunk_texts)
    chunk_table_name = Collection.get_chunk_table_name(collection_id)

    # make different timestamps for each chunk
    current_timestamp = current_timestamp_int_milliseconds()
    timestamps = [current_timestamp + i for i in range(len(chunk_texts))]

    insert_values_sql = ", ".join(
        [
            f"("
            f"${i * 8 + 1}, "
            f"${i * 8 + 2}, "
            f"${i * 8 + 3}, "
            f"${i * 8 + 4}, "
            f"${i * 8 + 5}, "
            f"${i * 8 + 6}, "
            f"${i * 8 + 7}, "
            f"${i * 8 + 8}"
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
                json.dumps(chunk_embeddings[i]),
                chunk_texts[i],
                "{}",
                timestamps[i],
                timestamps[i],
            ]
        )

    # make the final insert sql
    insert_chunks_sql = f"""
        INSERT INTO {chunk_table_name}(chunk_id, record_id, collection_id, embedding, content,
         metadata, updated_timestamp, created_timestamp)
        VALUES {insert_values_sql};
    """

    # insert chunks
    await conn.execute(insert_chunks_sql, *params)


async def delete_record_chunks(conn, collection_id: str, record_id: str):
    """
    Delete record chunks
    :param conn:
    :param collection_id: the collection id
    :param record_id: the record id
    :return:
    """

    chunk_table_name = Collection.get_chunk_table_name(collection_id)

    await conn.execute(
        f"""
        DELETE FROM {chunk_table_name}
        WHERE record_id = $1
    """,
        record_id,
    )

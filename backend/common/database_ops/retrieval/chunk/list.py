from common.database.postgres.pool import postgres_db_pool


async def list_get_chunks(
    chunk_table_name: str,
):
    async with postgres_db_pool.get_db_connection() as conn:
        rows = await conn.fetch(
            f"""
            SELECT chunk_id, text, metadata, text_bytes, embedding_bytes FROM {chunk_table_name}
        """
        )

    # todo: update to Chunk model
    results = [
        {
            "chunk_id": row["chunk_id"],
            "text": row["text"],
            "metadata": row["metadata"],
            "text_bytes": row["text_bytes"],
            "embedding_bytes": row["embedding_bytes"],
        }
        for row in rows
    ]
    return results


async def list_get_record_chunks(chunk_table_name: str, record_id: str):
    async with postgres_db_pool.get_db_connection() as conn:
        rows = await conn.fetch(
            f"""
            SELECT chunk_id, text, metadata, text_bytes, embedding_bytes FROM {chunk_table_name}
            WHERE record_id = $1
        """,
            record_id,
        )

    # todo: update to Chunk model
    results = [
        {
            "chunk_id": row["chunk_id"],
            "text": row["text"],
            "metadata": row["metadata"],
            "text_bytes": row["text_bytes"],
            "embedding_bytes": row["embedding_bytes"],
        }
        for row in rows
    ]
    return results

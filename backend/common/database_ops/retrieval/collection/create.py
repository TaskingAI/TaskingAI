from common.database.postgres.pool import postgres_db_pool
from common.models import Collection, Status
from .get import get_collection
from typing import Dict
import json
import logging

logger = logging.getLogger(__name__)


async def create_collection(
    name: str,
    description: str,
    capacity: int,
    embedding_model_id: str,
    embedding_size: int,
    metadata: Dict[str, str],
) -> Collection:
    """
    Create collection
    :param name: the collection name
    :param description: the collection description
    :param capacity: the collection capacity
    :param embedding_model_id: the embedding model id
    :param embedding_size: the embedding size
    :param metadata: the collection metadata
    :return: the created collection
    """

    new_id = Collection.generate_random_id()
    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert the collection into database
            await conn.execute(
                """
                INSERT INTO collection (collection_id, name, description, capacity,
                embedding_model_id, embedding_size, status, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
                new_id,
                name,
                description,
                capacity,
                embedding_model_id,
                embedding_size,
                Status.READY.value,
                json.dumps(metadata),
            )

            chunk_table_name = Collection.get_chunk_table_name(new_id)
            create_chunk_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {chunk_table_name} (
                    chunk_id CHAR(24) NOT NULL PRIMARY KEY,
                    collection_id CHAR(24) NOT NULL,
                    record_id CHAR(24),
                    content TEXT NOT NULL,
                    metadata JSONB NOT NULL DEFAULT '{{}}',
                    embedding vector({embedding_size}) NOT NULL,
                    created_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
                    updated_timestamp BIGINT NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT,
                    FOREIGN KEY (collection_id, record_id) REFERENCES record (collection_id, record_id) ON DELETE CASCADE
                );
            """

        logging.debug(f"create_collection: create chunk table with: \n {create_chunk_table_sql}")

        # 2. create the chunk table
        await conn.execute(create_chunk_table_sql)

        # 3. todo: add index

    # 3. get and add to redis
    collection = await get_collection(new_id)
    return collection

from app.database.connection import postgres_pool
from app.models import Collection
from tkhelper.models import Status
from typing import Dict
import json
import logging
from ..chunk.utils import get_m_ef_construction

logger = logging.getLogger(__name__)


async def create_collection(
    collection_id: str,
    name: str,
    description: str,
    capacity: int,
    embedding_model_id: str,
    embedding_size: int,
    metadata: Dict[str, str],
):
    """
    Create collection
    :param collection_id: the collection id
    :param name: the collection name
    :param description: the collection description
    :param capacity: the collection capacity
    :param embedding_model_id: the embedding model id
    :param embedding_size: the embedding size
    :param metadata: the collection metadata
    :return: None
    """

    async with postgres_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert the collection into database
            await conn.execute(
                """
                INSERT INTO collection (collection_id, name, description, capacity,
                embedding_model_id, embedding_size, status, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
                collection_id,
                name,
                description,
                capacity,
                embedding_model_id,
                embedding_size,
                Status.READY.value,
                json.dumps(metadata),
            )

            chunk_table_name = Collection.get_chunk_table_name(collection_id)
            create_chunk_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {chunk_table_name} (
                    chunk_id CHAR(24) NOT NULL PRIMARY KEY,
                    collection_id CHAR(24) NOT NULL,
                    record_id CHAR(24),
                    content TEXT NOT NULL,
                    num_tokens INT NOT NULL DEFAULT 0,
                    extra JSONB NOT NULL DEFAULT '{{}}',
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

            # 3. add hnsw vector index
            m, ef_construction = get_m_ef_construction(capacity, embedding_size)
            await conn.execute(
                f"""
                CREATE INDEX ON {chunk_table_name}
                USING hnsw (embedding vector_cosine_ops)
                WITH (m = {m}, ef_construction = {ef_construction});
             """
            )
            logger.debug(f"create_collection: create hnsw index with m={m}, ef_construction={ef_construction}")

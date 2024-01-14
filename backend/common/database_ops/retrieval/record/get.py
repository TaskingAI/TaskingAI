from common.database.postgres.pool import postgres_db_pool
from common.models import Record, Collection


async def get_record(collection: Collection, record_id: str):
    # 1. get from db
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM record WHERE collection_id = $1 AND record_id = $2", collection.collection_id, record_id
        )

    # 2. return if exists
    if row:
        record = Record.build(row)
        return record

    return None

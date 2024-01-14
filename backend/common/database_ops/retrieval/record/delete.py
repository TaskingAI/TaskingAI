from common.database.postgres.pool import postgres_db_pool
from common.models import Record


async def delete_record(record: Record):
    # 1. delete from db
    async with postgres_db_pool.get_db_connection() as conn:
        await conn.execute(
            "DELETE FROM record WHERE collection_id=$1 AND record_id=$2;", record.collection_id, record.record_id
        )

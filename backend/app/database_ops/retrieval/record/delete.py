from app.database.connection import postgres_pool
from app.models import Record
from .utils import delete_record_chunks


async def delete_record(record: Record):
    async with postgres_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. delete record chunks
            old_num_chunks = await delete_record_chunks(conn, record.collection_id, record.record_id)

            # 2. delete from db
            await conn.execute(
                "DELETE FROM record WHERE collection_id=$1 AND record_id=$2;",
                record.collection_id,
                record.record_id,
            )

            # 3. update vectordb_collection num_records and num_chunks
            await conn.execute(
                "UPDATE collection "
                "SET num_records = num_records - 1, num_chunks = num_chunks - $1 "
                "WHERE collection_id=$2;",
                old_num_chunks,
                record.collection_id,
            )

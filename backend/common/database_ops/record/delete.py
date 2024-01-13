from common.models.record import Record
from common.database.redis import redis_object_pop


async def delete_record(postgres_conn, record: Record):
    # 1. pop from redis
    await redis_object_pop(Record, record.record_id)

    # 2. delete from db
    await postgres_conn.execute("DELETE FROM record WHERE record_id=$1;", record.record_id)

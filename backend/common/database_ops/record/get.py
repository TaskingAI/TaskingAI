from common.models import Record, SerializePurpose
from common.database.redis import redis_object_get_object, redis_object_set_object


async def get_record(conn, record_id: str):
    # 1. get from redis
    record: Record = await redis_object_get_object(Record, key=record_id)
    if record:
        return record

    # 2. get from db
    row = await conn.fetchrow(
        """
        SELECT * FROM record WHERE record_id = $1
    """,
        record_id,
    )

    # 3. write to redis and return
    if row:
        record = Record.build(row)
        await redis_object_set_object(Record, key=record_id, value=record.to_dict(purpose=SerializePurpose.REDIS))
        return record

    return None

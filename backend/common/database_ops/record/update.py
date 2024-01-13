from common.models.record import Record
from typing import Dict
from common.database.redis import redis_object_pop
from ..utils import update_object
from .get import get_record
from common.database.redis import redis_object_pop


async def update_record(conn, record: Record, update_dict: Dict):
    # 1. pop from redis
    await redis_object_pop(Record, record.record_id)

    # 2. Update record in database
    await update_object(
        conn,
        update_dict=update_dict,
        update_time=True,
        table_name="record",
        condition_fields={"record_id": record.record_id},
    )

    # 3. Get updated record
    record = await get_record(conn, record.record_id)

    return record

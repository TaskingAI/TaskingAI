from common.database.postgres.pool import postgres_db_pool
from common.models import Record, Collection
from typing import Dict
from common.database_ops.utils import update_object
from .get import get_record


async def update_record(collection: Collection, record: Record, update_dict: Dict):
    # 1. Update record in database
    async with postgres_db_pool.get_db_connection() as conn:
        await update_object(
            conn,
            update_dict=update_dict,
            update_time=True,
            table_name="record",
            condition_fields={"collection_id": record.collection_id, "record_id": record.record_id},
        )

    # 2. Get updated record
    record = await get_record(collection, record.record_id)

    return record

from common.database.postgres.pool import postgres_db_pool
from common.models import Collection
from typing import Dict
from common.database_ops.utils import update_object
from .get import get_collection
from common.database.redis import redis_object_pop


async def update_collection(collection: Collection, update_dict: Dict):
    # 1. pop from redis
    await redis_object_pop(Collection, collection.collection_id)

    # 2. Update collection in database
    async with postgres_db_pool.get_db_connection() as conn:
        await update_object(
            conn,
            update_dict=update_dict,
            update_time=True,
            table_name="collection",
            condition_fields={"collection_id": collection.collection_id},
        )

    # 3. Get updated collection
    collection = await get_collection(collection.collection_id)

    return collection

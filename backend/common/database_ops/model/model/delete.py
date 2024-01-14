from common.database.postgres.pool import postgres_db_pool
from common.models import Model
from common.database.redis import redis_object_pop


async def delete_model(
    model: Model,
):
    async with postgres_db_pool.get_db_connection() as conn:
        # 1. delete from db
        await conn.execute("DELETE FROM model WHERE model_id=$1;", model.model_id)

    # 2. pop from redis
    await redis_object_pop(Model, model.model_id)

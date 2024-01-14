from common.database.postgres.pool import postgres_db_pool
from common.models import Model, SerializePurpose
from common.database.redis import redis_object_get_object, redis_object_set_object


async def get_model(
    model_id: str,
):
    # 1. get from redis
    model: Model = await redis_object_get_object(Model, key=model_id)
    if model:
        return model

    async with postgres_db_pool.get_db_connection() as conn:
        # 2. get from db
        row = await conn.fetchrow(
            "SELECT * FROM model WHERE model_id = $1",
            model_id,
        )

    # 3. write to redis and return
    if row:
        model = Model.build(row)
        await redis_object_set_object(Model, key=model_id, value=model.to_dict(purpose=SerializePurpose.REDIS))
        return model

    return None

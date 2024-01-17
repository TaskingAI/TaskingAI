from common.database.postgres.pool import postgres_db_pool
from common.models import Model


async def get_model(
    model_id: str,
):
    # 1. get from redis
    model: Model = await Model.get_redis(model_id)
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
        await model.set_redis()
        return model

    return None

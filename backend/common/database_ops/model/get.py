from common.models import Model
from .redis import redis_get_model, redis_set_model


async def get_model(
    conn,
    model_id: str,
):
    # 1. get from redis
    model: Model = await redis_get_model(model_id)
    if model:
        return model

    # 2. get from db
    row = await conn.fetchrow(
        """
        SELECT * FROM model WHERE model_id = $1
    """,
        model_id,
    )

    # 3. write to redis and return
    if row:
        model = Model.build(row)
        await redis_set_model(model=model)
        return model

    return None

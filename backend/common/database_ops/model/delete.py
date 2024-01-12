from common.models import Model
from .redis import redis_pop_model


async def delete_model(conn, model: Model):
    # 1. delete from db
    await conn.execute("DELETE FROM model WHERE model_id=$1;", model.model_id)

    # 2. pop from redis
    await redis_pop_model(model=model)

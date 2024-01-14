from common.models import Model
from common.database.redis import redis_object_pop


async def delete_model(conn, model: Model):
    # 1. delete from db
    await conn.execute("DELETE FROM model WHERE model_id=$1;", model.model_id)

    # 2. pop from redis
    await redis_object_pop(Model, model.model_id)

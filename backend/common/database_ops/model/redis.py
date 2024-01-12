from common.database.redis import redis_object_get_object, redis_object_set_object, redis_object_pop
from common.models import Model, SerializePurpose


async def redis_get_model(model_id: str):
    aimodel: Model = await redis_object_get_object(Model, key=model_id)
    return aimodel


async def redis_set_model(model: Model):
    await redis_object_set_object(Model, key=model.model_id, value=model.to_dict(purpose=SerializePurpose.REDIS))


async def redis_pop_model(model: Model):
    await redis_object_pop(Model, key=model.model_id)

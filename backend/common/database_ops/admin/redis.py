from common.database.redis import redis_object_get_object, redis_object_set_object, redis_object_pop
from common.models import Admin, SerializePurpose


async def get_redis_admin_by_id(admin_id: str):
    redis_admin: Admin = await redis_object_get_object(Admin, key=admin_id)
    return redis_admin


async def get_redis_admin_by_username(username: str):
    redis_admin: Admin = await redis_object_get_object(Admin, key=username)
    return redis_admin


async def set_redis_admin(admin: Admin):
    await redis_object_set_object(Admin, key=admin.username, value=admin.to_dict(purpose=SerializePurpose.REDIS))
    await redis_object_set_object(Admin, key=admin.admin_id, value=admin.to_dict(purpose=SerializePurpose.REDIS))


async def pop_redis_admin(admin: Admin):
    await redis_object_pop(Admin, key=admin.username)
    await redis_object_pop(Admin, key=admin.admin_id)

from .connection import redis_pool
import json
import logging

logger = logging.getLogger(__name__)


def _real_key(ObjectClass, key: str):
    return f"{ObjectClass.object_name()}:{key}"


def _build_object_from_value_dict(ObjectClass, value: dict):
    try:
        return ObjectClass.build(value)
    except Exception as e:
        raise Exception(f"_build_object_from_value_dict: error={e}")


async def redis_object_set_int(ObjectClass, key: str, value: int, expire: int = 3600 * 4):
    if redis_pool.redis is None:
        return
    try:
        real_key = _real_key(ObjectClass, key)
        await redis_pool.redis.set(real_key, value)
        if expire:
            await redis_pool.redis.expire(real_key, expire)
    except Exception as e:
        logger.error(f"redis_object_set_int: error={e}")


async def redis_object_set_object(ObjectClass, key: str, value: dict, expire: int = 3600 * 4):
    if redis_pool.redis is None:
        return
    try:
        real_key = _real_key(ObjectClass, key)
        await redis_pool.redis.set(real_key, json.dumps(value))
        if expire:
            await redis_pool.redis.expire(real_key, expire)
    except Exception as e:
        logger.error(f"redis_object_set_object: error={e}")


async def redis_object_set_string(ObjectClass, key: str, value: str, expire: int = 3600 * 4):
    if redis_pool.redis is None:
        return
    try:
        real_key = _real_key(ObjectClass, key)
        await redis_pool.redis.set(real_key, value)
        if expire:
            await redis_pool.redis.expire(real_key, expire)
    except Exception as e:
        logger.error(f"redis_object_set_string: error={e}")


async def redis_object_pop(ObjectClass, key: str):
    if redis_pool.redis is None:
        return
    try:
        real_key = _real_key(ObjectClass, key)
        await redis_pool.redis.delete(real_key)
    except Exception as e:
        logger.error(f"redis_object_pop: error={e}")


async def redis_object_get_string(ObjectClass, key: str):
    if redis_pool.redis is None:
        return
    try:
        real_key = _real_key(ObjectClass, key)
        value_string = await redis_pool.redis.get(real_key)
        return value_string
    except Exception as e:
        logger.error(f"redis_object_get_string: error={e}")


async def redis_object_get_object(ObjectClass, key: str):
    if redis_pool.redis is None:
        return
    try:
        real_key = _real_key(ObjectClass, key)
        value_string = await redis_pool.redis.get(real_key)
        if value_string:
            return _build_object_from_value_dict(ObjectClass, json.loads(value_string))
    except Exception as e:
        logger.error(f"redis_object_get_object: error={e}")
    return None


async def redis_object_get_int(ObjectClass, key: str):
    if redis_pool.redis is None:
        return
    try:
        real_key = _real_key(ObjectClass, key)
        value = await redis_pool.redis.get(real_key)
        if value:
            return int(value)
    except Exception as e:
        logger.error(f"redis_object_get_int: error={e}")
    return None

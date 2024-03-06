import aioredis
from aioredis import Redis
import json
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class RedisConnection:
    def __init__(self, url: str):
        self.url = url
        self.redis: Redis = None

    # -- connection management --

    async def init(self):
        self.redis = await aioredis.from_url(self.url)
        await self.redis.config_set("maxmemory-policy", "allkeys-lru")
        logger.info("Set redis maxmemory-policy to allkeys-lru")
        logger.info("Redis pool initialized.")

    async def close(self):
        if self.redis is not None:
            await self.redis.close()
            logger.info("Redis pool closed.")

    # -- clean --

    async def clean_data(self):
        await self.redis.flushdb()
        logger.info("Redis flush done.")

    # -- operations --

    # Redis operations
    async def set_int(self, key: str, value: int, expire: int = 3600 * 4):
        if self.redis is None:
            return
        try:
            await self.redis.set(key, value)
            if expire:
                await self.redis.expire(key, expire)
            logger.debug(f"set_int: key={key}, value={value}")
        except Exception as e:
            logger.error(f"set_int: error={e}")

    async def set_object(self, key: str, value: Dict, expire: int = 3600 * 4):
        if self.redis is None:
            return
        try:
            await self.redis.set(key, json.dumps(value))
            if expire:
                await self.redis.expire(key, expire)
            logger.debug(f"set_object: key={key}, value={value}")
        except Exception as e:
            logger.error(f"set_object: error={e}")

    async def set_string(self, key: str, value: str, expire: int = 3600 * 4):
        if self.redis is None:
            return
        try:
            await self.redis.set(key, value)
            if expire:
                await self.redis.expire(key, expire)
            logger.debug(f"set_string: key={key}, value={value}")
        except Exception as e:
            logger.error(f"set_string: error={e}")

    async def pop(self, key: str):
        if self.redis is None:
            return
        try:
            await self.redis.delete(key)
            logger.debug(f"pop: key={key}")
        except Exception as e:
            logger.error(f"pop: error={e}")

    async def get_string(self, key: str):
        if self.redis is None:
            return None
        try:
            value_string = await self.redis.get(key)
            logger.debug(f"get_string: key={key}, value={value_string}")
            return value_string
        except Exception as e:
            logger.error(f"get_string: error={e}")
            return None

    async def get_object(self, key: str) -> Optional[Dict]:
        if self.redis is None:
            return None
        try:
            value_string = await self.redis.get(key)
            logger.debug(f"get_object: key={key}, value={value_string}")
            if value_string:
                return json.loads(value_string)
        except Exception as e:
            logger.error(f"get_object: error={e}")
            return None

    async def get_int(self, key: str):
        if self.redis is None:
            return None
        try:
            value = await self.redis.get(key)
            logger.debug(f"get_int: key={key}, value={value}")
            if value:
                return int(value)
        except Exception as e:
            logger.error(f"get_int: error={e}")
            return None

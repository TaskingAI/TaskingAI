import aioredis
from config import CONFIG
from aioredis import Redis

import logging

logger = logging.getLogger(__name__)


class RedisPool:
    def __init__(self):
        self.redis: Redis = None

    async def init_pool(self):
        self.redis = await aioredis.from_url(CONFIG.REDIS_URL)
        await self.redis.config_set("maxmemory-policy", "allkeys-lru")
        logger.info("Set redis maxmemory-policy to allkeys-lru")
        logger.info("Redis pool initialized.")

    async def clean_data(self):
        await self.redis.flushdb()
        logger.info("Redis flushdb done.")

    async def close_pool(self):
        if self.redis is not None:
            await self.redis.close()
            logger.info("Redis pool closed.")


redis_pool = RedisPool()

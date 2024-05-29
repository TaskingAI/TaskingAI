from tkhelper.database.redis import RedisConnection
from typing import Optional, Type
from .entity import ModelEntity
import logging

logger = logging.getLogger(__name__)

__all__ = ["RedisOperator"]


class RedisOperator(object):
    def __init__(
        self,
        entity_class: Type[ModelEntity],
        redis_conn: RedisConnection = None,
        redis_key_postfix: str = None,
        expire: int = 3600 * 4,
    ):
        self.entity_class = entity_class
        self.redis_conn = redis_conn
        self.redis_key_postfix = redis_key_postfix
        self.expire = expire

    # --- redis ---

    def __key(self, postfix: str = None, **kwargs) -> str:
        """Generate a Redis key based on the object name, primary key fields, and an optional postfix."""
        # Start with the object name
        key_parts = [self.entity_class.object_name()]

        # Add the primary key components in the specified order
        for field in self.entity_class.primary_key_fields():
            if field in kwargs:
                key_parts.append(str(kwargs[field]))
            else:
                raise ValueError(f"Missing value for primary key field: {field}")

        # If a postfix is provided, append it
        if postfix:
            key_parts.append(postfix)

        # Join all parts with a colon
        return ":".join(key_parts)

    async def get(self, **kwargs) -> Optional[ModelEntity]:
        if not self.redis_conn:
            return None
        key = self.__key(self.redis_key_postfix, **kwargs)
        data = await self.redis_conn.get_object(key)
        if data:
            try:
                return self.entity_class.build(data)
            except Exception as e:
                logger.error(f"Error building entity from Redis data: {e}")
                await self.redis_conn.pop(key)
        return None

    async def set(self, entity: ModelEntity):
        if not self.redis_conn:
            return

        # Extract primary key fields and their values from entity
        pk_fields = self.entity_class.primary_key_fields()
        pk_values = {field: getattr(entity, field) for field in pk_fields}

        # Generate the Redis key using primary key values
        key = self.__key(**pk_values, postfix=self.redis_key_postfix)

        # Convert entity to a dictionary suitable for Redis (assuming such a method exists)
        entity_dict = entity.to_redis_dict()  # This method depends on the actual implementation of ModelEntity

        # Set the object in Redis with the generated key and expiration
        await self.redis_conn.set_object(key, entity_dict, self.expire)

    async def pop(self, entity: ModelEntity):
        if not self.redis_conn:
            return

        # Extract primary key fields and their values from entity
        pk_fields = self.entity_class.primary_key_fields()
        pk_values = {field: getattr(entity, field) for field in pk_fields}

        # Generate the Redis key using primary key values
        key = self.__key(**pk_values, postfix=self.redis_key_postfix)

        # Remove the object from Redis using the generated key
        await self.redis_conn.pop(key)

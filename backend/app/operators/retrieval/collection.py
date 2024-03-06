from tkhelper.models import RedisOperator
from tkhelper.models.operator.postgres_operator import PostgresModelOperator

from app.database import redis_conn, postgres_pool
from app.models import Collection


__all__ = [
    "collection_ops",
]


collection_ops = PostgresModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Collection,
    redis=RedisOperator(
        entity_class=Collection,
        redis_conn=redis_conn,
    ),
)

from tkhelper.models import RedisOperator
from tkhelper.models.operator.postgres_operator import PostgresModelOperator

from app.database import postgres_pool, redis_conn
from app.models import Admin

__all__ = ["admin_ops"]


admin_ops = PostgresModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Admin,
    redis=RedisOperator(
        entity_class=Admin,
        redis_conn=redis_conn,
    ),
)

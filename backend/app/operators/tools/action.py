from tkhelper.models import RedisOperator
from tkhelper.models.operator.postgres_operator import PostgresModelOperator

from app.database import redis_conn, postgres_pool
from app.models import Action

__all__ = ["action_ops"]

action_ops = PostgresModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Action,
    redis=RedisOperator(
        entity_class=Action,
        redis_conn=redis_conn,
    ),
)

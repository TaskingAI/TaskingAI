from tkhelper.models.operator.postgres_operator import PostgresModelOperator

from app.database import postgres_pool
from app.models import Record


__all__ = ["record_ops"]


record_ops = PostgresModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Record,
    redis=None,
)

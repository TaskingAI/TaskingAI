from tkhelper.models.operator.postgres_operator import PostgresModelOperator

from app.database import postgres_pool
from app.models import Chunk


__all__ = [
    "chunk_ops",
]


chunk_ops = PostgresModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Chunk,
    redis=None,
)

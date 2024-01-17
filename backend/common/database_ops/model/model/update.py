from common.database.postgres.pool import postgres_db_pool
from common.models import Model
from typing import Dict
from common.database_ops.utils import update_object


async def update_model(
    model: Model,
    update_dict: Dict,
):
    # 1. Invalidate cache
    await model.pop_redis()

    async with postgres_db_pool.get_db_connection() as conn:
        # 2. Update database
        await update_object(
            conn, update_dict, update_time=True, table_name="model", equal_filters={"model_id": model.model_id}
        )

    # 3. Update aimodel model
    for key, value in update_dict.items():
        setattr(model, key, value)

    return model

from common.models import Model
from typing import Dict
from common.database.redis import redis_object_pop
from ..utils import update_object


async def update_model(conn, model: Model, update_dict: Dict):
    # 1. Invalidate cache
    await redis_object_pop(Model, key=model.model_id)

    # 2. Update database
    await update_object(
        conn, update_dict, update_time=True, table_name="model", condition_fields={"model_id": model.model_id}
    )

    # 3. Update aimodel model
    for key, value in update_dict.items():
        setattr(model, key, value)

    return model

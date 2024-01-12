from common.models import Model
from typing import Dict
from .redis import redis_pop_model
from ..utils import prepare_and_execute_update


async def update_model(conn, model: Model, update_dict: Dict):
    # 1. Invalidate cache
    await redis_pop_model(model=model)

    # 2. Update database
    await prepare_and_execute_update(
        conn, update_dict, update_time=True, table_name="model", condition_fields={"model_id": model.model_id}
    )

    # 3. Update aimodel model
    for key, value in update_dict.items():
        setattr(model, key, value)

    return model

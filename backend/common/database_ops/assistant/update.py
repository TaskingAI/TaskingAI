from common.models.assistant import Assistant
from typing import Dict
from ..utils import update_object
from .get import get_assistant
from common.database.redis import redis_object_pop


async def update_assistant(conn, assistant: Assistant, update_dict: Dict):
    # 1. pop from redis
    await redis_object_pop(Assistant, assistant.assistant_id)

    # 2. Update assistant in database
    await update_object(
        conn,
        update_dict=update_dict,
        update_time=True,
        table_name="assistant",
        condition_fields={"assistant_id": assistant.assistant_id},
    )

    # 3. Get updated assistant
    assistant = await get_assistant(conn, assistant.assistant_id)

    return assistant

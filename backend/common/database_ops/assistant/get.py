from common.models import Assistant, SerializePurpose
from common.database.redis import redis_object_get_object, redis_object_set_object


async def get_assistant(conn, assistant_id: str):
    # 1. get from redis
    assistant: Assistant = await redis_object_get_object(Assistant, key=assistant_id)
    if assistant:
        return assistant

    # 2. get from db
    row = await conn.fetchrow(
        "SELECT * FROM assistant WHERE assistant_id = $1",
        assistant_id,
    )

    # 3. write to redis and return
    if row:
        assistant = Assistant.build(row)
        await redis_object_set_object(
            Assistant, key=assistant_id, value=assistant.to_dict(purpose=SerializePurpose.REDIS)
        )
        return assistant

    return None

import json
from common.database.postgres.pool import postgres_db_pool
from common.models import Model, ModelType
from .get import get_model
from typing import Dict


async def create_model(
    model_schema_id: str,
    provider_id: str,
    provider_model_id: str,
    name: str,
    type: ModelType,
    encrypted_credentials: Dict,
    display_credentials: Dict,
    properties: Dict,
):
    new_id = Model.generate_random_id()

    async with postgres_db_pool.get_db_connection() as conn:
        # 1. create model in db
        await conn.execute(
            """
            INSERT INTO model (
                model_id,
                model_schema_id,
                provider_id,
                provider_model_id,
                name,
                type,
                encrypted_credentials,
                display_credentials,
                properties
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """,
            new_id,
            model_schema_id,
            provider_id,
            provider_model_id,
            name,
            type.value,
            json.dumps(encrypted_credentials),
            json.dumps(display_credentials),
            json.dumps(properties),
        )

    # 2. get and add to redis
    model = await get_model(new_id)

    return model

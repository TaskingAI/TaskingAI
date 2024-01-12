import json

from common.models import Model
from .get import get_model
from typing import Dict


async def create_model(
    conn,
    model_schema_id: str,
    provider_id: str,
    provider_model_id: str,
    name: str,
    encrypted_credentials: Dict,
    display_credentials: Dict,
):
    new_id = Model.generate_random_id()

    # 1. create model in db
    await conn.execute(
        """
        INSERT INTO model (
            model_id, model_schema_id, provider_id, provider_model_id, name, encrypted_credentials, display_credentials
        ) VALUES ($1, $2, $3, $4, $5, $6, $7);
    """,
        new_id,
        model_schema_id,
        provider_id,
        provider_model_id,
        name,
        json.dumps(encrypted_credentials),
        json.dumps(display_credentials),
    )

    # 2. get and add to redis
    model = await get_model(conn, new_id)

    return model

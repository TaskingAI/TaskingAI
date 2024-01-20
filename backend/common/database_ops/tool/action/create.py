from common.database.postgres.pool import postgres_db_pool
from common.models import Action, Authentication
from .get import get_action
from typing import Dict, List, Tuple
import json
from common.utils import current_timestamp_int_milliseconds


async def create_actions(
    actions: List[Tuple[Dict, str, str]],
    authentication: Authentication,
) -> List[Action]:
    """
    Create actions
    :param actions: List of (openapi_schema, name, description)
    :param authentication: the authentication for the action
    :return: List of actions
    """

    # 1. ensure the authentication is encrypted
    if not authentication.is_encrypted():
        raise Exception("Authentication must be encrypted")

    action_ids = []
    current_timestamp = current_timestamp_int_milliseconds()

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # create actions in db
            for openapi_schema, name, description in actions:
                # insert action
                action_id = Action.generate_random_id()
                await conn.execute(
                    """
                    INSERT INTO action (
                        action_id, name, description, openapi_schema, authentication,
                        updated_timestamp, created_timestamp
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                    action_id,
                    name,
                    description,
                    json.dumps(openapi_schema),
                    authentication.model_dump_json(),
                    current_timestamp,
                    current_timestamp,
                )
                action_ids.append(action_id)

                # make different timestamps for each action
                current_timestamp += 1

    # 2. get and add to redis
    actions = []
    for action_id in action_ids:
        action = await get_action(action_id)
        actions.append(action)

    return actions

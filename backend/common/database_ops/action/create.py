from common.models import Action, Authentication
from .get import get_action
from typing import Dict, List, Tuple
import json


async def create_actions(
    postgres_conn,
    actions: List[Tuple[Dict, str, str]],
    authentication: Authentication,
) -> List[Action]:
    """
    Create actions
    :param postgres_conn: postgres connection
    :param actions: List of (openapi_schema, name, description)
    :param authentication: the authentication for the action
    :return: List of actions
    """

    # 1. ensure the authentication is encrypted
    if not authentication.is_encrypted():
        raise Exception("Authentication must be encrypted")

    action_ids = []

    async with postgres_conn.transaction():
        # create actions in db
        for openapi_schema, name, description in actions:
            action_id = Action.generate_random_id()
            await postgres_conn.execute(
                """
                INSERT INTO action (
                    action_id, name, description, openapi_schema, authentication
                ) VALUES ($1, $2, $3, $4, $5);
            """,
                action_id,
                name,
                description,
                json.dumps(openapi_schema),
                authentication.model_dump_json(),
            )
            action_ids.append(action_id)

    # 2. get and add to redis
    actions = []
    for action_id in action_ids:
        action = await get_action(postgres_conn, action_id)
        actions.append(action)

    return actions

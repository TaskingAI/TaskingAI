from common.database.postgres.pool import postgres_db_pool
from common.models import Action, Authentication, ActionStruct, action_param_schema_to_dict
from .get import get_action
from typing import List
import json
from common.utils import current_timestamp_int_milliseconds


async def create_actions(
    action_structs: List[ActionStruct],
    authentication: Authentication,
) -> List[Action]:
    """
    Create actions
    :param action_structs: List of ActionStruct
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
            for struct in action_structs:
                # insert action
                action_id = Action.generate_random_id()
                await conn.execute(
                    """
                    INSERT INTO action (
                        action_id, openapi_schema, authentication,
                        name, description, operation_id, url, method,
                        path_param_schema, query_param_schema, body_type, body_param_schema, function_def,
                        updated_timestamp, created_timestamp
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9,
                              $10, $11, $12, $13, $14, $15)
                """,
                    action_id,
                    json.dumps(struct.openapi_schema),
                    authentication.model_dump_json(),
                    struct.name,
                    struct.description,
                    struct.operation_id,
                    struct.url,
                    struct.method,
                    json.dumps(action_param_schema_to_dict(struct.path_param_schema)),
                    json.dumps(action_param_schema_to_dict(struct.query_param_schema)),
                    struct.body_type,
                    json.dumps(action_param_schema_to_dict(struct.body_param_schema)),
                    struct.function_def.model_dump_json(),
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

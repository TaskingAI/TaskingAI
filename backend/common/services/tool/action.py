from typing import Optional, Dict, List
from common.models import Action, Authentication, SortOrderEnum, ListResult
from common.database_ops.tool import action as db_action
from common.error import ErrorCode, raise_http_error
from .openapi_utils import split_openapi_schema, extract_function_description
from .openapi_call import call_action_api


__all__ = [
    "list_actions",
    "bulk_create_actions",
    "update_action",
    "get_action",
    "delete_action",
    "run_action",
]


async def validate_and_get_action(action_id: str) -> Action:
    action = await db_action.get_action(action_id)
    if not action:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Action {action_id} not found.")
    return action


async def list_actions(
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    id_search: Optional[str],
    name_search: Optional[str],
) -> ListResult:
    """
    List actions
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :param offset: the offset of the query
    :param id_search: the action ID to search for
    :param name_search: the action name to search for
    :return: a list of actions, total count of actions, and whether there are more actions
    """

    after_action, before_action = None, None

    if after:
        after_action = await validate_and_get_action(after)

    if before:
        before_action = await validate_and_get_action(before)

    return await db_action.list_actions(
        limit=limit,
        order=order,
        after_action=after_action,
        before_action=before_action,
        offset=offset,
        prefix_filters={
            "action_id": id_search,
            "name": name_search,
        },
    )


async def bulk_create_actions(
    openapi_schema: Dict,
    authentication: Authentication,
) -> List[Action]:
    schemas = split_openapi_schema(openapi_schema)
    if not schemas:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Failed to parse OpenAPI schema")

    action_tuples = []
    for schema in schemas:
        function = extract_function_description(schema)
        action_tuples.append((schema, function["name"], function["description"]))

    actions = await db_action.create_actions(
        actions=action_tuples,
        authentication=authentication,
    )
    return actions


async def update_action(
    action_id: str,
    openapi_schema: Dict,
    authentication: Authentication,
) -> Action:
    action: Action = await validate_and_get_action(action_id=action_id)

    update_dict = {}
    if openapi_schema:
        update_dict["openapi_schema"] = openapi_schema
        function_desc = extract_function_description(openapi_schema)
        update_dict["name"] = function_desc["name"]
        update_dict["description"] = function_desc["description"]

    if authentication:
        update_dict["authentication"] = authentication.model_dump()

    action = await db_action.update_action(
        action=action,
        update_dict=update_dict,
    )
    return action


async def get_action(action_id: str) -> Action:
    action: Action = await validate_and_get_action(action_id)
    return action


async def delete_action(action_id: str) -> None:
    action: Action = await validate_and_get_action(action_id)
    await db_action.delete_action(action)


async def run_action(action_id: str, parameters: Dict, headers: Dict) -> Dict:
    """
    Run an action
    :param action_id: the action ID
    :param parameters: the parameters for the API call
    :param headers: the headers for the API call
    :return: the response of the API call
    """
    action: Action = await validate_and_get_action(action_id=action_id)
    response = await call_action_api(
        openapi_schema=action.openapi_schema,
        authentication=action.authentication,
        parameters=parameters,
        headers=headers,
    )
    return response

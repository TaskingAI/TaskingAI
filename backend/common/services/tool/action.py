from typing import Optional, Dict, List
from common.models import Action, Authentication, SortOrderEnum, ListResult, ActionStruct, action_param_schema_to_dict
from common.database_ops.tool import action as db_action
from common.error import ErrorCode, raise_http_error
from .openapi_utils import split_openapi_schema, build_action_struct, replace_openapi_refs
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
    openapi_schema = replace_openapi_refs(openapi_schema)
    schemas = split_openapi_schema(openapi_schema)
    if not schemas:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Failed to parse OpenAPI schema")

    action_structs = []
    for schema in schemas:
        action_struct = build_action_struct(schema)
        action_structs.append(action_struct)

    actions = await db_action.create_actions(
        action_structs=action_structs,
        authentication=authentication,
    )
    return actions


async def update_action(
    action_id: str,
    openapi_schema: Optional[Dict] = None,
    authentication: Optional[Authentication] = None,
) -> Action:
    action: Action = await validate_and_get_action(action_id)

    update_dict = {}

    if openapi_schema is not None:
        openapi_schema = replace_openapi_refs(openapi_schema)
        action_struct: ActionStruct = build_action_struct(openapi_schema)
        update_dict["openapi_schema"] = action_struct.openapi_schema
        update_dict["name"] = action_struct.name
        update_dict["description"] = action_struct.description
        update_dict["url"] = action_struct.url
        update_dict["method"] = action_struct.method.value
        update_dict["path_param_schema"] = action_param_schema_to_dict(action_struct.path_param_schema)
        update_dict["query_param_schema"] = action_param_schema_to_dict(action_struct.query_param_schema)
        update_dict["body_type"] = action_struct.body_type.value
        update_dict["body_param_schema"] = action_param_schema_to_dict(action_struct.body_param_schema)
        update_dict["function_def"] = action_struct.function_def.model_dump()

    if authentication is not None:
        update_dict["authentication"] = authentication.model_dump()

    action = await db_action.update_action(
        action=action,
        update_dict=update_dict,
    )
    return action


async def get_action(action_id: str) -> Action:
    action: Action = await validate_and_get_action(action_id)

    if not action.operation_id:
        #  renew action data
        try:
            action = await update_action(
                action_id=action_id,
                openapi_schema=action.openapi_schema,
            )
        except Exception as e:
            raise_http_error(
                ErrorCode.INVALID_REQUEST,
                message=f"The OpenAPI schema of action {action_id} is invalid. Please update.",
            )

    return action


async def delete_action(action_id: str) -> None:
    action: Action = await validate_and_get_action(action_id)
    await db_action.delete_action(action)


async def run_action(
    action_id: str,
    parameters: Dict,
    headers: Dict,
) -> Dict:
    """
    Run an action
    :param action_id: the action ID
    :param parameters: the parameters for the API call
    :param headers: the headers for the API call
    :return: the response of the API call
    """
    action: Action = await validate_and_get_action(action_id)

    response = await call_action_api(
        url=action.url,
        method=action.method,
        path_param_schema=action.path_param_schema,
        query_param_schema=action.query_param_schema,
        body_param_schema=action.body_param_schema,
        body_type=action.body_type,
        parameters=parameters,
        headers=headers,
        authentication=action.authentication,
    )
    return response

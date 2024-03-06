from typing import Optional, Dict, List
from app.models import Action, ActionAuthentication
from app.operators import action_ops
from tkhelper.error import ErrorCode, raise_http_error
from tkhelper.utils import current_timestamp_int_milliseconds
from .openapi_utils import split_openapi_schema, build_action_struct, replace_openapi_refs
from .openapi_call import call_action_api


__all__ = [
    "bulk_create_actions",
    "update_action",
    "run_action",
]


async def bulk_create_actions(
    openapi_schema: Dict,
    authentication: ActionAuthentication,
) -> List[Action]:
    openapi_schema = replace_openapi_refs(openapi_schema)
    schemas = split_openapi_schema(openapi_schema)
    if not schemas:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message="Failed to parse OpenAPI schema",
        )

    create_dict_list = []
    authentication_dict = authentication.model_dump()
    timestamp = current_timestamp_int_milliseconds()

    for i, schema in enumerate(schemas):
        action_struct = build_action_struct(schema)

        path_param_dict = None
        if action_struct.path_param_schema:
            path_param_dict = {k: v.model_dump() for k, v in action_struct.path_param_schema.items()}

        query_param_dict = None
        if action_struct.query_param_schema:
            query_param_dict = {k: v.model_dump() for k, v in action_struct.query_param_schema.items()}

        body_param_dict = None
        if action_struct.body_param_schema:
            body_param_dict = {k: v.model_dump() for k, v in action_struct.body_param_schema.items()}

        create_dict = {
            "openapi_schema": action_struct.openapi_schema,
            "authentication": authentication_dict,
            "name": action_struct.name,
            "description": action_struct.description,
            "operation_id": action_struct.operation_id,
            "url": action_struct.url,
            "method": action_struct.method,
            "path_param_schema": path_param_dict,
            "query_param_schema": query_param_dict,
            "body_type": action_struct.body_type,
            "body_param_schema": body_param_dict,
            "function_def": action_struct.function_def.model_dump(),
            "created_timestamp": timestamp,
            "updated_timestamp": timestamp,
        }
        timestamp += 1
        create_dict_list.append(create_dict)

    actions = await action_ops.bulk_create(
        create_dict_list=create_dict_list,
    )
    return actions


async def update_action(
    action_id: str,
    openapi_schema: Optional[Dict],
    authentication: Optional[ActionAuthentication],
) -> Action:
    """
    Update an action
    :param action_id: the action ID
    :param openapi_schema: an OpenAPI schema which should only contain one path with one method
    :param authentication: the authentication for the API call
    :return:
    """

    update_dict = {}

    if authentication is not None:
        update_dict["authentication"] = authentication.model_dump()

    if openapi_schema is not None:
        openapi_schema = replace_openapi_refs(openapi_schema)
        schemas = split_openapi_schema(openapi_schema)
        if not schemas:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                message="Failed to parse OpenAPI schema",
            )
        if len(schemas) > 1:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                message="The OpenAPI schema should contain only one path with one method.",
            )
        schema = schemas[0]

        action_struct = build_action_struct(schema)

        path_param_dict = None
        if action_struct.path_param_schema:
            path_param_dict = {k: v.model_dump() for k, v in action_struct.path_param_schema.items()}

        query_param_dict = None
        if action_struct.query_param_schema:
            query_param_dict = {k: v.model_dump() for k, v in action_struct.query_param_schema.items()}

        body_param_dict = None
        if action_struct.body_param_schema:
            body_param_dict = {k: v.model_dump() for k, v in action_struct.body_param_schema.items()}

        update_dict.update(
            {
                "openapi_schema": action_struct.openapi_schema,
                "name": action_struct.name,
                "description": action_struct.description,
                "operation_id": action_struct.operation_id,
                "url": action_struct.url,
                "method": action_struct.method,
                "path_param_schema": path_param_dict,
                "query_param_schema": query_param_dict,
                "body_type": action_struct.body_type,
                "body_param_schema": body_param_dict,
                "function_def": action_struct.function_def.model_dump(),
            }
        )

    action = await action_ops.update(
        action_id=action_id,
        update_dict=update_dict,
    )
    return action


async def run_action(
    action_id: str,
    parameters: Dict,
) -> Dict:
    """
    Run an action
    :param action_id: the action ID
    :param parameters: the parameters for the API call
    :return: the response of the API call
    """
    action: Action = await action_ops.get(action_id=action_id)

    response = await call_action_api(
        url=action.url,
        method=action.method,
        path_param_schema=action.path_param_schema,
        query_param_schema=action.query_param_schema,
        body_param_schema=action.body_param_schema,
        body_type=action.body_type,
        parameters=parameters,
        headers={},  # todo add headers
        authentication=action.authentication,
    )
    return response

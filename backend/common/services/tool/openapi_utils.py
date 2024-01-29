import json
import re
from typing import Dict, Tuple, Optional
import copy
import logging
from common.models import ActionStruct, ActionMethod, ActionBodyType, ActionParam, ChatCompletionFunction
from common.error import raise_http_error, ErrorCode

logger = logging.getLogger(__name__)


def validate_param_type(param_name: str, param_type: str):
    # check var type in [string, integer, number, boolean] but not object or array
    if param_type not in ["string", "integer", "number", "boolean"]:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR, f"Param {param_name}'s type {param_type} is not supported."
        )


def _resolve_ref(document, ref):
    parts = ref.split("/")
    result = document
    for part in parts[1:]:
        result = result[part]
    return result


def _replace_refs(schema, document):
    if isinstance(schema, dict):
        if "$ref" in schema:
            ref_path = schema["$ref"]
            return _resolve_ref(document, ref_path)
        else:
            return {k: _replace_refs(v, document) for k, v in schema.items()}
    elif isinstance(schema, list):
        return [_replace_refs(item, document) for item in schema]
    else:
        return schema


def replace_openapi_refs(openapi_dict) -> Dict:
    processed_dict = _replace_refs(openapi_dict, openapi_dict)

    if "components" in processed_dict:
        del processed_dict["components"]

    return processed_dict


def split_openapi_schema(openapi_schema: Dict):
    # Check if the original JSON has 'paths' and 'servers' fields
    if "paths" not in openapi_schema or "servers" not in openapi_schema:
        return []

    base_json = {
        "openapi": openapi_schema.get("openapi", "3.0.0"),
        "info": openapi_schema.get("info", {}),
        "servers": openapi_schema.get("servers", []),
        "components": openapi_schema.get("components", {}),
        "security": openapi_schema.get("security", []),
    }

    split_jsons = []

    for path, methods in openapi_schema["paths"].items():
        for method, details in methods.items():
            # deep copy the base json
            new_json = json.loads(json.dumps(base_json))
            # only keep one path and method
            new_json["paths"] = {path: {method: details}}
            split_jsons.append(new_json)

    return split_jsons


def _to_snake_case(name):
    # Convert CamelCase to snake_case
    temp = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", temp).lower()


def _function_name(method, path, operation_id=None):
    if operation_id:
        # Use operationId and convert to snake_case
        return _to_snake_case(operation_id)

    # Remove leading and trailing slashes and split the path
    path_parts = path.strip("/").split("/")

    # Replace path parameters (such as {userId}) with 'by'
    path_parts = [re.sub(r"{\w+}", "by", part) for part in path_parts]

    # Combine the method and path parts into an underscore-separated string
    snake_case_name = "_".join([method.lower()] + path_parts)

    return snake_case_name


def check_single_value_enum(param_schema: Dict) -> bool:
    """
    check if the parameter schema has a single value enum
    :param param_schema: The parameter schema dictionary.
    :return: a boolean indicating if the parameter schema has a single value enum
    """
    if "enum" in param_schema and isinstance(param_schema["enum"], list):
        if len(param_schema["enum"]) == 1:
            return True
    return False


def _build_function_def(
    name: str,
    description: str,
    path_param_schema: Dict,
    query_param_schema: Dict,
    body_param_schema: Dict,
) -> ChatCompletionFunction:
    """
    Build a function definition from provided schemas and metadata.
    :param name: the name of the function
    :param description: the description of the function
    :param path_param_schema: the path parameters schema
    :param query_param_schema: the query parameters schema
    :param body_param_schema: the body parameters schema
    :return: a dict of function definition
    """

    parameters_schema = {"type": "object", "properties": {}, "required": []}

    # Process and add path and query params to the schema
    for param_schemas in [path_param_schema, query_param_schema, body_param_schema]:
        if not param_schemas:
            continue
        for param_name, action_param in param_schemas.items():
            if not action_param.is_single_value_enum():
                parameters_schema["properties"][param_name] = action_param.model_dump(exclude_none=True)
                if action_param.required:
                    parameters_schema["required"].append(param_name)

    function_def = ChatCompletionFunction(
        name=name,
        description=description,
        parameters=parameters_schema,
    )

    return function_def


def _extract_params(
    openapi_schema: Dict,
    method: ActionMethod,
    path: str,
) -> Tuple[
    str,
    Optional[Dict[str, ActionParam]],
    Optional[Dict[str, ActionParam]],
    ActionBodyType,
    Optional[Dict[str, ActionParam]],
]:
    """
    Extract parameter schemas for an API call based on OpenAPI schema definitions.

    :param openapi_schema: The OpenAPI specification as a dictionary.
    :param method: The HTTP method as an instance of ActionMethod.
    :param path: The API endpoint path.
    :return: A tuple with the final URL, path_param_schema, query_param_schema, body_type, and body_param_schema.

    """

    # Extract base URL from OpenAPI schema and construct final endpoint URL
    base_url = openapi_schema["servers"][0]["url"]
    final_url = f"{base_url}{path}"

    path_param_schema = None
    query_param_schema = None
    body_param_schema = None
    body_type = ActionBodyType.NONE

    # Verify if the provided path exists in the OpenAPI schema
    path_item = openapi_schema["paths"].get(path)
    if path_item is None:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"No path item found for path: {path}")

    # Verify if the provided method is defined for the path in the OpenAPI schema
    operation = path_item.get(method.value.lower())
    if operation is None:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"No operation found for method: {method} at path: {path}")

    # Extract schemas for path and query parameters
    if "parameters" in operation:
        for param in operation["parameters"]:
            param_name = param["name"]
            param_in = param["in"]
            param_type = param["schema"]["type"]
            validate_param_type(param_name, param_type)
            action_param = ActionParam(
                type=param_type,
                description=param.get("description", ""),
                required=param.get("required", False),
                enum=param["schema"].get("enum"),
            )
            if param_in == "query":
                if query_param_schema is None:
                    query_param_schema = {}
                query_param_schema[param_name] = action_param
            elif param_in == "path":
                if path_param_schema is None:
                    path_param_schema = {}
                path_param_schema[param_name] = action_param

    # Extract information about the requestBody
    if "requestBody" in operation:
        content_types = operation["requestBody"]["content"].keys()
        original_body_param_schema = None
        if "application/json" in content_types:
            body_type = ActionBodyType.JSON
            original_body_param_schema = operation["requestBody"]["content"]["application/json"].get("schema", {})
        elif "application/x-www-form-urlencoded" in content_types:
            body_type = ActionBodyType.FORM
            original_body_param_schema = operation["requestBody"]["content"]["application/x-www-form-urlencoded"].get(
                "schema", {}
            )
        if original_body_param_schema:
            body_param_schema = {}
            for prop_name, prop_info in original_body_param_schema.get("properties", {}).items():
                param_type = prop_info.get("type")
                validate_param_type(prop_name, param_type)
                body_param_schema[prop_name] = ActionParam(
                    type=param_type,
                    description=prop_info.get("description", ""),
                    enum=prop_info.get("enum", None),
                    required=prop_name in original_body_param_schema.get("required", []),
                )

    return final_url, path_param_schema, query_param_schema, body_type, body_param_schema


def build_action_struct(
    openapi_schema: Dict,
) -> ActionStruct:
    """
    Extract action components from OpenAPI schema.
    :param openapi_schema: a dict of OpenAPI schema
    :return: an ActionStruct including all the components of an action
    """

    # copy openapi_schema to avoid modifying the original
    openapi_dict = copy.deepcopy(openapi_schema)

    # extract the first path and method
    path, path_info = next(iter(openapi_dict["paths"].items()))
    method, method_info = next(iter(path_info.items()))

    # check operationId
    operation_id = method_info.get("operationId", None)

    # get function name
    name = _function_name(method, path, operation_id)
    method = ActionMethod(method.upper())

    # extract description
    description = method_info.get("description", "")
    if not description:
        # use other fields to generate description
        summary = method_info.get("summary", "")
        description = f"{method.upper()} {path}: {summary}"

    # build function parameters schema
    url, path_param_schema, query_param_schema, body_type, body_param_schema = _extract_params(
        openapi_dict, method, path
    )

    # build function definition
    function_def = _build_function_def(
        name=name,
        description=description,
        path_param_schema=path_param_schema,
        query_param_schema=query_param_schema,
        body_param_schema=body_param_schema,
    )

    return ActionStruct(
        name=name,
        description=description,
        operation_id=operation_id,
        url=url,
        method=method,
        path_param_schema=path_param_schema,
        query_param_schema=query_param_schema,
        body_type=body_type,
        body_param_schema=body_param_schema,
        function_def=function_def,
        openapi_schema=openapi_dict,
    )

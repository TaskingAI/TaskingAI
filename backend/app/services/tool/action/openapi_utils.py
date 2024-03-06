import json
import re
from typing import Dict, Tuple, Optional
import copy
import logging
from app.models import (
    ActionStruct,
    ActionMethod,
    ActionBodyType,
    ChatCompletionFunction,
    ActionParam,
)


logger = logging.getLogger(__name__)

__all__ = [
    "replace_openapi_refs",
    "split_openapi_schema",
    "build_action_struct",
]


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


def _build_function_def(
    name: str,
    description: str,
    path_param_schema: Optional[Dict[str, ActionParam]],
    query_param_schema: Optional[Dict[str, ActionParam]],
    body_param_schema: Optional[Dict[str, ActionParam]],
) -> ChatCompletionFunction:
    """
    Build a function definition from provided schemas and metadata.
    :param name: the name of the function
    :param description: the description of the function
    :param path_param_schema: the path parameters schema, which is a dict of ActionParam
    :param query_param_schema: the query parameters schema, which is a dict of ActionParam
    :param body_param_schema: the body parameters schema, which is a dict of ActionParam
    :return: a dict of function definition, which is compliant with ChatCompletionFunction
    """

    parameters_dict = {"type": "object", "properties": {}, "required": []}

    # Process and add path and query params to the schema
    for param_schemas in [path_param_schema, query_param_schema, body_param_schema]:
        if not param_schemas:
            continue
        for param_name, param_schema in param_schemas.items():
            single_value_enum = param_schema.enum and len(param_schema.enum) == 1
            if not single_value_enum:
                parameters_dict["properties"][param_name] = {
                    "type": param_schema.type,
                    "description": param_schema.description,
                    "enum": param_schema.enum,
                }
                if param_schema.required:
                    parameters_dict["required"].append(param_name)

    function_definition = ChatCompletionFunction(
        name=name,
        description=description,
        parameters=parameters_dict,
    )

    return function_definition


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
    :raises ValueError: If the path or method is not found in the OpenAPI schema.
    """

    # Extract base URL from OpenAPI schema and construct final endpoint URL
    base_url = openapi_schema["servers"][0]["url"]
    final_url = f"{base_url}{path}"

    path_param_dict = {}
    query_param_dict = {}
    body_param_dict = {}
    body_type = ActionBodyType.NONE

    # Verify if the provided path exists in the OpenAPI schema
    path_item = openapi_schema["paths"].get(path)
    if path_item is None:
        raise ValueError(f"No path item found for path: {path}")

    # Verify if the provided method is defined for the path in the OpenAPI schema
    operation = path_item.get(method.value.lower())
    if operation is None:
        raise ValueError(f"No operation found for method: {method} at path: {path}")

    # Extract schemas for path and query parameters
    if "parameters" in operation:
        for param in operation["parameters"]:
            param_name = param["name"]
            param_in = param["in"]
            param_required = param.get("required", False)
            param_description = param.get("description", "")
            param_type = param.get("schema", {}).get("type", "string")
            param_enum_list = param.get("schema", {}).get("enum", None)

            param = ActionParam(
                type=param_type,
                description=param_description,
                enum=param_enum_list,
                required=param_required,
            )

            if param_in == "query":
                query_param_dict[param_name] = param

            elif param_in == "path":
                path_param_dict[param_name] = param

    # Extract information about the requestBody
    body = None
    if "requestBody" in operation:
        content_types = operation["requestBody"]["content"].keys()
        if "application/json" in content_types:
            body_type = ActionBodyType.JSON
            body = operation["requestBody"]["content"]["application/json"].get("schema", {})
        elif "application/x-www-form-urlencoded" in content_types:
            body_type = ActionBodyType.FORM
            body = operation["requestBody"]["content"]["application/x-www-form-urlencoded"].get("schema", {})

    body_properties = (body or {}).get("properties", {})
    if body_properties:
        body_required = body.get("required", [])
        for param_name, param_schema in body_properties.items():
            param = ActionParam(
                type=param_schema.get("type", "string"),
                description=param_schema.get("description", ""),
                enum=param_schema.get("enum", None),
                required=param_name in body_required,
            )

            body_param_dict[param_name] = param

    return final_url, path_param_dict or None, query_param_dict or None, body_type, body_param_dict or None


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

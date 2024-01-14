import json
import re
from typing import Dict
import copy
import logging

logger = logging.getLogger(__name__)


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


def function_format(openapi_schema: Dict):
    # copy openapi_schema to avoid modifying the original
    openapi_dict = copy.deepcopy(openapi_schema)

    # extract the first path and method
    path, path_info = next(iter(openapi_dict["paths"].items()))
    method, method_info = next(iter(path_info.items()))

    # check operationId
    operation_id = method_info.get("operationId", None)

    # get function name
    function_name = _function_name(method, path, operation_id)

    # extract description
    description = method_info.get("description", "")
    if not description:
        # use other fields to generate description
        summary = method_info.get("summary", "")
        description = f"{method.upper()} {path} {summary}"

    # build function parameters schema
    parameters_schema = {"type": "object", "properties": {}, "required": []}

    for param in method_info.get("parameters", []):
        name = param["name"]
        param_schema = param["schema"]
        param_schema["description"] = param.get("description", "")
        parameters_schema["properties"][name] = param_schema
        if param.get("required", False):
            parameters_schema["required"].append(name)

    # build function description
    function_description = {"name": function_name, "description": description, "parameters": parameters_schema}

    return function_description

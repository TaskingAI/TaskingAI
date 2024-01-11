from typing import List, Dict
import re
import openapi_spec_validator
from common.error import raise_http_error, ErrorCode


def check_update_keys(data: Dict, keys: List[str]):
    if not any([(data.get(key) is not None) for key in keys]):
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="At least one field should be filled")


def validate_identifier(identifier: str):
    r = "^[a-zA-Z_][a-zA-Z0-9_]*$"

    if not re.match(r, identifier):
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Invalid identifier {identifier}")

    return identifier


def validate_openapi_schema(schema: Dict, only_one_path_and_method: bool):
    try:
        openapi_spec_validator.validate(schema)
        # check exactly one server in the schema
    except Exception as e:
        if hasattr(e, "message"):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Invalid openapi schema: " + e.message)
        else:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Invalid openapi schema")

    if "servers" not in schema:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="No server is found in action schema")

    if "paths" not in schema:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="No paths is found in action schema")

    if len(schema["servers"]) != 1:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Exactly one server is allowed in action schema")

    if only_one_path_and_method:
        if len(schema["paths"]) != 1:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Only one path is allowed in action schema")
        path = list(schema["paths"].keys())[0]
        if len(schema["paths"][path]) != 1:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Only one method is allowed in action schema")

    # check each path method has a valid description and operationId
    for path, methods in schema["paths"].items():
        for method, details in methods.items():
            if not details.get("description") or not isinstance(details["description"], str):
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"No description is found in {method} {path} in action schema",
                )
            if len(details["description"]) > 512:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"Description cannot be longer than 512 characters in {method} {path} in action schema",
                )

            if not details.get("operationId") or not isinstance(details["operationId"], str):
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"No operationId is found in {method} {path} in action schema",
                )
            if len(details["operationId"]) > 128:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"operationId cannot be longer than 128 characters in {method} {path} in action schema",
                )

            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", details["operationId"]):
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f'Invalid operationId {details["operationId"]} in {method} {path} in action schema',
                )

    return schema


def validate_list_position_condition(data: Dict):
    if data.get("order") and (data["order"] not in ["asc", "desc"]):
        raise raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="order should be asc or desc")

    count = sum([1 for attr in ("after", "before", "offset") if data.get(attr) is not None])
    if count > 1:
        raise raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR, message="offset params cannot be used at the same time."
        )
    return data

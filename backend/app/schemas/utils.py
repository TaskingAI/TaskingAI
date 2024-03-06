from typing import Dict, List
import re
import json
from tkhelper.error import raise_http_error, ErrorCode

allowed_param_type = ["string", "number", "integer", "boolean"]
MAXIMUM_PARAMETER_DESCRIPTION_LENGTH = 300


def check_update_keys(data: Dict, keys: List[str]):
    if not any([(data.get(key) is not None) for key in keys]):
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="At least one field should be filled")


def validate_non_nested_json(json_dict: Dict):
    for key, value in json_dict.items():
        if isinstance(value, dict):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Nested JSON is not allowed in {key}")


def validate_identifier(identifier: str):
    r = "^[a-zA-Z_][a-zA-Z0-9_]*$"
    if not re.match(r, identifier):
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"{identifier} is an invalid identifier.")
    return identifier

    # valid = identifier.isidentifier() and identifier[0].islower() and len(identifier) <= 255
    # if not valid:
    #     raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message='Invalid identifier')


# get params like {{param}} from object
def get_params(string: str = None, string_list: List[str] = None, json_dict: Dict = None, json_list: List[Dict] = None):
    params = set()

    if string:
        params.update(re.findall("{{(.*?)}}", string))

    if string_list:
        for s in string_list:
            params.update(re.findall("{{(.*?)}}", s))

    if json_dict:
        # make json to string
        json_str = json.dumps(json_dict)
        params.update(re.findall("{{(.*?)}}", json_str))

    if json_list:
        for jd in json_list:
            # make json to string
            js = json.dumps(jd)
            params.update(re.findall("{{(.*?)}}", js))

    param_list = list(params)
    return param_list


def validate_prompt_template(prompt_template: List[str]):
    # check every item in prompt_template is string and not empty
    for item in prompt_template:
        if not isinstance(item, str):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Prompt template should be a list of string.")
        if not item:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Prompt template should not be empty.")


def validate_metadata(metadata: Dict):
    for k, v in metadata.items():
        if not isinstance(v, str):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Value '{v}' is not a string")
        if not isinstance(k, str):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Key '{k}' is not a string")
        if len(k) > 64:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Key '{k}' exceeds 64 characters")
        if len(v) > 512:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Value '{v}' exceeds 512 characters")
    return metadata


def validate_list_cursors(data: Dict):
    if data.get("order") and (data["order"] not in ["asc", "desc"]):
        raise ValueError("order should be asc or desc")

    count = sum([1 for attr in ("after", "before", "offset") if data.get(attr) is not None])
    if count > 1:
        raise ValueError("cursor params cannot be used at the same time.")
    return data

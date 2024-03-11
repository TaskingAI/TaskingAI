from starlette.requests import Request
from fastapi import HTTPException
from typing import Dict, Type, Tuple
from pydantic import ValidationError
import re
import json

from tkhelper.error import raise_http_error, ErrorCode, raise_request_validation_error
from tkhelper.models import ModelOperator, ModelEntity

from app.config import CONFIG
from app.services.auth.admin import verify_admin_token
from app.services.auth.apikey import verify_apikey


__all__ = [
    "check_http_error",
    "app_admin_auth_info_required",
    "api_auth_info_required",
    "auth_info_required",
    "check_path_params",
    "path_params_required",
    "validate_list_filter",
]


def check_http_error(response):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", {}))


async def app_admin_auth_info_required(request: Request) -> Dict:
    ret = {}

    # 1. extract token
    authorization = request.headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        ret["token"] = authorization[7:]

    if not ret.get("token"):
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Token is missing")

    # 2. verify token
    admin = await verify_admin_token(token=ret["token"])
    ret["admin_id"] = admin.admin_id

    return ret


async def api_auth_info_required(request: Request) -> Dict:
    apikey = None

    # 1. extract apikey
    authorization = request.headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        apikey = authorization[7:]

    if not apikey:
        raise_http_error(ErrorCode.APIKEY_VALIDATION_FAILED, message="API Key validation failed")

    # 2. verify apikey
    await verify_apikey(apikey=apikey)
    ret = {
        "apikey": apikey,
    }

    return ret


async def auth_info_required(request: Request) -> Dict:
    if CONFIG.WEB:
        return await app_admin_auth_info_required(request)

    elif CONFIG.API:
        return await api_auth_info_required(request)

    raise NotImplementedError("Unknown auth type")


alphanumeric_pattern = re.compile("^[_a-zA-Z0-9]+$")


def check_path_params(
    model_operator: ModelOperator,
    object_id_required: bool,
    path_params: Dict,
):
    """Check if kwargs contains all the primary key fields except the id field."""
    entity_class = model_operator.entity_class
    id_field_name = entity_class.id_field_name()
    primary_key_fields = entity_class.primary_key_fields()

    # Only the id field is required
    required_fields = [field for field in primary_key_fields if "id" in field]

    # If the id field is required, add it to the required fields
    for k in required_fields:
        if k not in path_params and (k != id_field_name or object_id_required):
            raise_request_validation_error(f"Missing path parameter: {k}")

    # check all oath params are alphanumeric
    for k, v in path_params.items():
        if not alphanumeric_pattern.match(v):
            raise_request_validation_error(f"Invalid path parameter: {k}")

    # Check each id field
    try:
        entity_class.validate_path_params(path_params)
    except ValidationError as exc:
        detail = exc.errors()[0]
        raise_request_validation_error(f"{detail['loc'][0]}: {detail['msg']}")

    return


async def path_params_required(request: Request) -> Dict[str, str]:
    if len(request.path_params) > 0:
        return request.path_params
    return {}


async def validate_list_filter(
    model_operator: ModelOperator,
    path_params: Dict,
    prefix_filter: str = "",
    equal_filter: str = "",
) -> Tuple[Dict, Dict]:
    # check parent objects exist
    entity_class = model_operator.entity_class
    for parent_model, parent_operator in zip(entity_class.parent_models(), entity_class.parent_operator()):
        parent_model: Type[ModelEntity]
        parent_operator: ModelOperator
        parent_id = path_params.get(parent_model.id_field_name())
        if not parent_id:
            raise_request_validation_error(f"Missing {parent_model.id_field_name()}")
        parent_entity = await parent_operator.get(**path_params)
        if not parent_entity:
            raise_request_validation_error(f"Parent {parent_model.object_name()} not found")

    prefix_filter_dict = {}
    equal_filter_dict = {}

    if CONFIG.API:
        if prefix_filter:
            raise_request_validation_error("Prefix filter is not supported")
        if equal_filter:
            raise_request_validation_error("Equal filter is not supported")

    # check prefix_filter keys
    if entity_class.list_prefix_filter_fields() and prefix_filter:
        try:
            prefix_filter_dict = json.loads(prefix_filter)
        except json.JSONDecodeError:
            raise_request_validation_error("Invalid prefix filter format")
        for k in prefix_filter_dict:
            if k not in entity_class.list_prefix_filter_fields():
                raise_request_validation_error(f"Invalid prefix filter: {k}")

    # check equal_filter keys
    if entity_class.list_equal_filter_fields() and equal_filter:
        try:
            equal_filter_dict = json.loads(equal_filter)
        except json.JSONDecodeError:
            raise_request_validation_error("Invalid equal filter format")
        for k in equal_filter_dict:
            if k not in entity_class.list_equal_filter_fields():
                raise_request_validation_error(f"Invalid equal filter: {k}")

    return prefix_filter_dict, equal_filter_dict

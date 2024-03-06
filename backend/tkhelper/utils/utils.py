import string
import random
import datetime
from typing import Dict, Any
from enum import Enum
import json
from starlette.requests import Request
from fastapi import HTTPException

__all__ = [
    "generate_random_id",
    "current_timestamp_int_milliseconds",
    "load_json_attr",
    "path_params_required",
    "ResponseWrapper",
    "check_http_error",
    "prepare_db_dict",
]


def generate_random_id(length):
    first_letter = string.ascii_uppercase + string.ascii_lowercase
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return random.choice(first_letter) + "".join(random.choice(letters) for _ in range(length - 1))


def current_timestamp_int_milliseconds():
    return round(datetime.datetime.now().timestamp() * 1000)


def load_json_attr(row: Dict, key: str, default_value: Any = None):
    data = row.get(key)
    if data:
        if isinstance(data, str):
            return json.loads(data)
        elif isinstance(data, dict) or isinstance(data, list):
            return data
        else:
            return default_value
    else:
        return default_value


class ResponseWrapper:
    def __init__(self, status: int, json_data: Dict):
        self.status_code = status
        self._json_data = json_data

    def json(self):
        return self._json_data


def check_http_error(response):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", {}))


def prepare_db_dict(data: Dict):
    upsert_dict = data.copy()
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            upsert_dict[key] = json.dumps(value)
        if isinstance(value, Enum):
            upsert_dict[key] = value.value
    return upsert_dict


async def path_params_required(request: Request) -> Dict[str, str]:
    if len(request.path_params) > 0:
        return request.path_params
    return {}

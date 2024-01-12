import string
import random
import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
import json


def generate_random_id(length):
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def current_timestamp_int_milliseconds():
    return int(datetime.datetime.now().timestamp() * 1000)


def load_json_attr(row: Dict, key: str, default_value: Any = None):
    data = row.get(key)
    if data:
        if isinstance(data, str):
            return json.loads(data)
        elif isinstance(data, dict):
            return data
        else:
            logger.error(f"load_json_dict: error, key={key}, data={data}, default_value={default_value}")
            return default_value
    else:
        return default_value


def load_normal_attr(row: Dict, key: str, default_value: Any = None):
    data = row.get(key)
    if data:
        return data
    else:
        return default_value

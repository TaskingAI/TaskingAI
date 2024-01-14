import string
import random
import datetime
from typing import Dict, Any
from fastapi import HTTPException
from config import CONFIG
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

import logging

logger = logging.getLogger(__name__)
AES_ENCRYPTION_KEY_BYTES = bytes.fromhex(CONFIG.AES_ENCRYPTION_KEY)


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
        elif isinstance(data, dict) or isinstance(data, list):
            return data
        else:
            logger.error(f"load_json_dict: error, key={key}, data={data}, default_value={default_value}")
            return default_value
    else:
        return default_value


def aes_encrypt(plain_text: str):
    cipher = AES.new(AES_ENCRYPTION_KEY_BYTES, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode("utf-8")
    ct = b64encode(ct_bytes).decode("utf-8")
    return f"{iv},{ct}"


def aes_decrypt(encrypted_text: str):
    if encrypted_text is None or "," not in encrypted_text:
        return None
    iv, ct = encrypted_text.split(",", 1)
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(AES_ENCRYPTION_KEY_BYTES, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode("utf-8")


class ResponseWrapper:
    def __init__(self, status: int, json_data: Dict):
        self.status_code = status
        self._json_data = json_data

    def json(self):
        return self._json_data


def check_http_error(response):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", {}))

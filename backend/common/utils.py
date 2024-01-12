import string
import random
import datetime
from typing import Dict, Any
import logging
from config import CONFIG

logger = logging.getLogger(__name__)
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

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

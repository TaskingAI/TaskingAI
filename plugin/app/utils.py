import time
import string
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from config import CONFIG
from app.error import ErrorCode, raise_http_error
import hashlib
import json

AES_ENCRYPTION_KEY_BYTES = bytes.fromhex(CONFIG.AES_ENCRYPTION_KEY)
LOWEST_MAX_TOKENS = 3

__all__ = [
    "get_current_timestamp_int",
    "generate_random_id",
    "generate_random_function_call_id",
    "aes_encrypt",
    "aes_decrypt",
    "handle_response",
]


def get_current_timestamp_int():
    return int(time.time() * 1000)


def generate_random_id(length):
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def generate_random_function_call_id():
    return "P3lf" + generate_random_id(20)


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


async def handle_response(response):
    """
    Handles the HTTP response, raising specific errors based on the response status and error type.

    :param response: The HTTP response object to handle.
    :raises: Raises specific errors based on the response status and error type.
    """
    if response.status != 200:
        result = await response.json()
        raise_http_error(
            ErrorCode.PROVIDER_ERROR,
            f"Error on calling provider model API: {result}",
        )


def checksum(data) -> str:
    """
    Returns the SHA256 checksum of the given data.

    :param data: The data to checksum.
    :return: The SHA256 checksum of the given data.
    """
    data_str = json.dumps(data, sort_keys=True)
    hash_object = hashlib.sha256()
    hash_object.update(data_str.encode())
    return hash_object.hexdigest()


def i18n_text(
    bundle_id: str,
    original: str,
    lang: str,
):
    from app.cache import get_i18n

    """
    Translate the original text to the target language using i18n.

    :param bundle_id: The provider ID.
    :param original: The original text.
    :param lang: The target language.
    :return: text in the target language.
    """
    if not lang:
        return original
    if original.startswith("i18n:"):
        return get_i18n(bundle_id, lang, original[5:])
    return original

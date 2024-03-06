import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

AES_ENCRYPTION_KEY = os.environ.get("AES_ENCRYPTION_KEY")
AES_ENCRYPTION_KEY_BYTES = None
if AES_ENCRYPTION_KEY:
    AES_ENCRYPTION_KEY_BYTES = bytes.fromhex(AES_ENCRYPTION_KEY)
else:
    raise Exception("AES_ENCRYPTION_KEY is not set")


def aes_encrypt(plain_text: str):
    if not AES_ENCRYPTION_KEY_BYTES:
        raise Exception("AES_ENCRYPTION_KEY is not set")
    cipher = AES.new(AES_ENCRYPTION_KEY_BYTES, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode("utf-8")
    ct = b64encode(ct_bytes).decode("utf-8")
    return f"{iv},{ct}"


def aes_decrypt(encrypted_text: str):
    if not AES_ENCRYPTION_KEY_BYTES:
        raise Exception("AES_ENCRYPTION_KEY is not set")
    if encrypted_text is None or "," not in encrypted_text:
        return None
    iv, ct = encrypted_text.split(",", 1)
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(AES_ENCRYPTION_KEY_BYTES, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode("utf-8")


def generate_aes_encryption_key():
    key_length = 32  # AES-256
    key = os.urandom(key_length)
    return key.hex()

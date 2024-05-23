from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import string
import random
from config import CONFIG

AES_ENCRYPTION_KEY_BYTES = bytes.fromhex(CONFIG.AES_ENCRYPTION_KEY)

__all__ = [
    "aes_encrypt",
    "aes_decrypt",
    "i18n_text",
    "generate_random_id",
]


def generate_random_id(length):
    """
    Generate a random ID.
    :param length: The length of the ID.
    :return: The random ID consisting of uppercase letters, lowercase letters, and digits.
    """
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def aes_encrypt(plain_text: str):

    """
    Encrypt the plain text using AES.
    :param plain_text: The plain text.
    :return: The encrypted text.
    """

    cipher = AES.new(AES_ENCRYPTION_KEY_BYTES, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode("utf-8")
    ct = b64encode(ct_bytes).decode("utf-8")
    return f"{iv},{ct}"


def aes_decrypt(encrypted_text: str):

    """
    Decrypt the encrypted text using AES.
    :param encrypted_text: The encrypted text.
    :return: The decrypted text.
    """

    if encrypted_text is None or "," not in encrypted_text:
        # no need to decrypt
        return encrypted_text

    iv, ct = encrypted_text.split(",", 1)
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(AES_ENCRYPTION_KEY_BYTES, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode("utf-8")


def i18n_text(
    provider_id: str,
    original: str,
    lang: str,
):
    from app.utils import get_i18n

    """
    Translate the original text to the target language using i18n.

    :param provider_id: The provider ID.
    :param original: The original text.
    :param lang: The target language.
    :return: text in the target language.
    """
    if not lang:
        return original
    if original.startswith("i18n:"):
        return get_i18n(provider_id, lang, original[5:])
    return original

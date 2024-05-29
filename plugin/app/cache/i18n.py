from typing import List, Dict
from config import CONFIG
from app.utils import checksum
import logging
logger = logging.getLogger(__name__)

__all__ = [
    "set_i18n",
    "get_i18n",
    "set_i18n_checksum",
    "get_i18n_cache",
    "get_i18n_checksum",
]

__i18n: Dict[str, str] = {}
__i18n_checksum: str = ""


def set_i18n(provider_id: str, lang: str, i18n: Dict[str, str]):
    """
    Set the i18n for the given plugin id and language.
    :param provider_id: provider id.
    :param lang: language.
    :param i18n: i18n dictionary.
    :return: None
    """

    for key, value in i18n.items():
        i18n_key = f"{provider_id}:{lang}:{key}"
        __i18n[i18n_key] = value


def set_i18n_checksum():
    """
    Set the i18n checksum.
    """
    global __i18n_checksum
    __i18n_checksum = checksum(__i18n)


def get_i18n(provider_id: str, lang: str, key: str):
    """
    Get the i18n for the given plugin id, language and key.
    :param provider_id: provider id.
    :param lang: language.
    :param key: key.
    :return: the i18n.
    """

    i18n_key = f"{provider_id}:{lang}:{key}"
    return (
        __i18n.get(i18n_key, "") or
        __i18n.get(f"{provider_id}:{CONFIG.DEFAULT_LANG}:{key}", "")
    )


def get_i18n_cache() -> Dict[str, str]:
    """
    Get the i18n cache.
    :return: the i18n cache.
    """
    return __i18n


def get_i18n_checksum() -> str:
    """
    Get the i18n checksum.
    :return: the i18n checksum.
    """
    return __i18n_checksum


from typing import Optional
from app.models import Bundle, Plugin
from app.config import CONFIG
import aiohttp
from tkhelper.utils import ResponseWrapper, check_http_error
from tkhelper.error import raise_http_error, ErrorCode
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "list_bundles",
    "list_plugins",
    "get_bundle",
    "get_plugin",
    "sync_plugin_data",
    "i18n_text",
]

_bundles, _plugins, _bundle_dict, _plugin_dict, _i18n_dict = [], [], {}, {}, {}
_bundle_plugin_dict = {}
_bundle_checksum, _plugin_checksum, _i18n_checksum = "", "", ""


async def sync_plugin_data():
    logger.debug(f"sync_plugin_data started!")

    global _bundle_checksum, _plugin_checksum, _i18n_checksum
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_PLUGIN_URL}/v1/cache_checksums",
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        response_data = response_wrapper.json()["data"]
        bundle_checksum = response_data["bundle_checksum"]
        plugin_checksum = response_data["plugin_checksum"]
        i18n_checksum = response_data["i18n_checksum"]
        if (
            bundle_checksum == _bundle_checksum
            and plugin_checksum == _plugin_checksum
            and i18n_checksum == _i18n_checksum
        ):
            logger.debug(f"Checksums are the same, no need to sync plugin data.")
            return

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_PLUGIN_URL}/v1/caches",
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        response_data = response_wrapper.json()["data"]

        # sort plugins by bundle_id, name
        plugins = [Plugin.build(plugin_data) for plugin_data in response_data["plugins"]]
        plugins.sort(key=lambda x: (x.bundle_id, x.plugin_id))

        num_plugins_dict = {}
        for plugin in plugins:
            num_plugins_dict[plugin.bundle_id] = num_plugins_dict.get(plugin.bundle_id, 0) + 1

        # sort bundles by bundle_id
        bundles = [Bundle.build(bundle_data) for bundle_data in response_data["bundles"]]
        bundles.sort(key=lambda x: x.bundle_id)

        i18n_dict = response_data["i18n"]

        for bundle in bundles:
            bundle.num_plugins = num_plugins_dict.get(bundle.bundle_id, 0)

    # sort bundle by name
    bundle_dict = {bundle.bundle_id: bundle for bundle in bundles}

    plugin_dict = {f"{plugin.bundle_id}:{plugin.plugin_id}": plugin for plugin in plugins}

    bundle_plugin_dict = {plugin.bundle_id: [] for plugin in plugins}
    for plugin in plugins:
        bundle_plugin_dict[plugin.bundle_id].append(plugin)
    for bundle_id in bundle_plugin_dict:
        # sort plugins by plugin_id
        bundle_plugin_dict[bundle_id].sort(key=lambda x: x.plugin_id)

    # update data
    global _bundles, _plugins, _bundle_dict, _plugin_dict, _i18n_dict, _bundle_plugin_dict
    _bundles = bundles
    _plugins = plugins
    _bundle_dict = bundle_dict
    _plugin_dict = plugin_dict
    _bundle_plugin_dict = bundle_plugin_dict
    _i18n_dict = i18n_dict

    # update checksum
    _bundle_checksum = bundle_checksum
    _plugin_checksum = plugin_checksum
    _i18n_checksum = i18n_checksum

    logger.debug(f"sync_plugin_data succeeded!")


def list_bundles(
    limit: int,
    offset: Optional[int],
):
    """
    List bundles.
    :param limit: the maximum number of bundles to return.
    :param offset: the offset of bundles to return.
    :return: a list of bundles.
    """

    # Paginate
    end_index = offset + limit
    page = _bundles[offset:end_index] or []

    # Check if there's more
    has_more = end_index < len(_bundles)

    return page, len(_bundles), has_more


def list_plugins(
    bundle_id: Optional[str],
):
    """
    List plugins by bundle_id.

    :param bundle_id: the bundle id to filter by.
    :return: a list of plugins
    """

    plugins = _bundle_plugin_dict.get(bundle_id, None)
    if plugins is None:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Bundle {bundle_id} not found.")

    return plugins


def get_bundle(bundle_id: str) -> Optional[Bundle]:
    """
    Get a bundle by bundle_id.

    :param bundle_id: the bundle id.
    :return: the bundle or None if not found.
    """
    return _bundle_dict.get(bundle_id)


def get_plugin(bundle_id: str, plugin_id: str) -> Optional[Plugin]:
    """
    Get a plugin

    :param bundle_id: the bundle id.
    :param plugin_id: the plugin id.
    :return: the plugin or None if not found.
    """
    return _plugin_dict.get(f"{bundle_id}:{plugin_id}")


def i18n_text(
    bundle_id: str,
    original: str,
    lang: str,
):
    """
    Translate the original text to the target language using i18n.

    :param bundle_id: The bundle ID.
    :param original: The original text.
    :param lang: The target language.
    :return: text in the target language.
    """
    global _i18n_dict
    if original.startswith("i18n:"):
        key = original[5:]
        i18n_key = f"{bundle_id}:{lang}:{key}"
        return _i18n_dict.get(i18n_key, "") or _i18n_dict.get(f"{bundle_id}:{CONFIG.DEFAULT_LANG}:{key}", "")

    return original

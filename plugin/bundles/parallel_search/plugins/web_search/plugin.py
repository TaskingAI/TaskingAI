import asyncio
import json
from urllib.parse import urlsplit

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.exceptions import McpError

from bundle_dependency import (
    BundleCredentials,
    ErrorCode,
    PluginHandler,
    PluginInput,
    PluginOutput,
    raise_http_error,
    raise_provider_api_error,
)
from config import CONFIG

MCP_ENDPOINT = "https://search.parallel.ai/mcp"
MCP_TIMEOUT_SECONDS = 90
MAX_SEARCH_QUERIES = 5
MAX_QUERY_LENGTH = 200
MAX_OUTPUT_BYTES = 100 * 1024


async def _reject_redirects(response: httpx.Response):
    if response.has_redirect_location:
        raise httpx.HTTPStatusError(
            "Redirects are disabled for the fixed Parallel Search MCP endpoint.",
            request=response.request,
            response=response,
        )


class WebSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        objective = plugin_input.input_params.get("objective")
        if not isinstance(objective, str) or not objective.strip():
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "objective must be a non-empty string.")

        search_queries = plugin_input.input_params.get("search_queries")
        if not isinstance(search_queries, list) or not 1 <= len(search_queries) <= MAX_SEARCH_QUERIES:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                f"search_queries must contain between 1 and {MAX_SEARCH_QUERIES} queries.",
            )

        normalized_queries = []
        for query in search_queries:
            if not isinstance(query, str) or not query.strip() or len(query.strip()) > MAX_QUERY_LENGTH:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    f"Each search query must contain 1 to {MAX_QUERY_LENGTH} characters.",
                )
            normalized_queries.append(query.strip())

        try:
            result = await asyncio.wait_for(
                self._call_search(objective.strip(), normalized_queries),
                timeout=MCP_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            raise_provider_api_error("Parallel Search MCP request timed out.")
        except httpx.TimeoutException:
            raise_provider_api_error("Parallel Search MCP request timed out.")
        except httpx.HTTPStatusError as error:
            raise_provider_api_error(f"Parallel Search MCP returned HTTP {error.response.status_code}.")
        except httpx.HTTPError:
            raise_provider_api_error("Parallel Search MCP could not be reached.")
        except McpError:
            raise_provider_api_error("Parallel Search MCP returned a JSON-RPC error.")
        except Exception:
            raise_provider_api_error("Parallel Search MCP request failed.")

        if getattr(result, "isError", False):
            raise_provider_api_error("Parallel Search MCP returned a tool error.")

        payload = getattr(result, "structuredContent", None)
        if payload is None:
            text_blocks = [
                block.text
                for block in getattr(result, "content", [])
                if getattr(block, "type", None) == "text" and isinstance(getattr(block, "text", None), str)
            ]
            if len(text_blocks) != 1:
                raise_provider_api_error("Parallel Search MCP returned an invalid search response.")
            try:
                payload = json.loads(text_blocks[0])
            except json.JSONDecodeError:
                raise_provider_api_error("Parallel Search MCP returned an invalid search response.")

        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise_provider_api_error("Parallel Search MCP returned an invalid search response.")

        results = []
        for item in payload["results"]:
            if not isinstance(item, dict):
                raise_provider_api_error("Parallel Search MCP returned an invalid search result.")

            url = item.get("url")
            if not isinstance(url, str):
                raise_provider_api_error("Parallel Search MCP returned an invalid source URL.")
            try:
                parsed_url = urlsplit(url)
            except ValueError:
                raise_provider_api_error("Parallel Search MCP returned an invalid source URL.")
            if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
                raise_provider_api_error("Parallel Search MCP returned an invalid source URL.")

            excerpts = item.get("excerpts")
            if not isinstance(excerpts, list) or not all(isinstance(excerpt, str) for excerpt in excerpts):
                raise_provider_api_error("Parallel Search MCP returned invalid source excerpts.")

            result_item = {"url": url, "excerpts": excerpts}
            for optional_field in ("title", "publish_date"):
                value = item.get(optional_field)
                if value is not None:
                    if not isinstance(value, str):
                        raise_provider_api_error("Parallel Search MCP returned invalid result metadata.")
                    result_item[optional_field] = value
            results.append(result_item)

        warnings = payload.get("warnings")
        if warnings is None:
            warnings = []

        try:
            results_json = json.dumps(results, ensure_ascii=False)
            warnings_json = json.dumps(warnings, ensure_ascii=False)
        except (TypeError, ValueError):
            raise_provider_api_error("Parallel Search MCP returned an invalid search response.")

        response_size = len(results_json.encode("utf-8")) + len(warnings_json.encode("utf-8"))
        if response_size > MAX_OUTPUT_BYTES:
            raise_provider_api_error("Parallel Search MCP response exceeded the supported size limit.")

        return PluginOutput(data={"results": results_json, "warnings": warnings_json})

    async def _call_search(self, objective: str, search_queries: list[str]):
        async with httpx.AsyncClient(
            headers={"User-Agent": f"TaskingAI/{CONFIG.VERSION}"},
            timeout=httpx.Timeout(60.0, connect=10.0, write=10.0, pool=10.0),
            proxy=CONFIG.PROXY or None,
            trust_env=False,
            follow_redirects=False,
            event_hooks={"response": [_reject_redirects]},
        ) as http_client:
            async with streamable_http_client(
                MCP_ENDPOINT,
                http_client=http_client,
                terminate_on_close=True,
            ) as (read_stream, write_stream, _):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    return await session.call_tool(
                        "web_search",
                        arguments={"objective": objective, "search_queries": search_queries},
                    )

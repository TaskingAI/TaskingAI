import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


@pytest.fixture(scope="module", autouse=True)
def load_parallel_search_schema():
    os.environ.setdefault("OBJECT_STORAGE_TYPE", "local")
    os.environ.setdefault("HOST_URL", "http://localhost")
    from app.cache import load_bundle_data, load_plugin_data

    load_bundle_data()
    load_plugin_data(["parallel_search"])


class _MCPFixtureServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self):
        super().__init__(("127.0.0.1", 0), _MCPFixtureHandler)
        self.requests = []
        self.payload = {"results": [], "warnings": []}
        self.is_error = False
        self.text_only = False
        self.jsonrpc_error = False
        self.include_output_schema = True
        self.redirect_initialize = False


class _MCPFixtureHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _record(self, request):
        headers = {name.lower(): value for name, value in self.headers.items()}
        self.server.requests.append({"request": request, "headers": headers, "path": self.path})

    def _respond(self, payload, status=200, headers=None):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length))
        self._record(request)
        method = request.get("method")

        if method == "notifications/initialized":
            self.send_response(202)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if self.server.redirect_initialize and method == "initialize":
            location = f"http://127.0.0.1:{self.server.server_address[1]}/redirect-target"
            self._respond({}, status=307, headers={"Location": location})
            return

        if method == "initialize":
            self._respond(
                {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": {
                        "protocolVersion": request["params"]["protocolVersion"],
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "local-search-fixture", "version": "1.0"},
                    },
                }
            )
            return

        if method == "tools/list":
            tool = {
                "name": "web_search",
                "description": "Search the public web.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "objective": {"type": "string"},
                        "search_queries": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["objective", "search_queries"],
                },
            }
            if self.server.include_output_schema:
                tool["outputSchema"] = {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "url": {"type": "string"},
                                    "excerpts": {"type": "array", "items": {"type": "string"}},
                                    "title": {"type": "string"},
                                    "publish_date": {"type": "string"},
                                },
                                "required": ["url", "excerpts"],
                            },
                        },
                        "warnings": {"type": ["array", "null"]},
                    },
                    "required": ["results"],
                }
            self._respond({"jsonrpc": "2.0", "id": request["id"], "result": {"tools": [tool]}})
            return

        if method == "tools/call":
            if self.server.jsonrpc_error:
                self._respond(
                    {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "error": {"code": -32000, "message": "search unavailable"},
                    }
                )
                return

            content = [{"type": "text", "text": json.dumps(self.server.payload)}]
            result = {"content": content}
            if not self.server.text_only:
                result["structuredContent"] = self.server.payload
            if self.server.is_error:
                result["isError"] = True
            self._respond({"jsonrpc": "2.0", "id": request["id"], "result": result})
            return

        self._respond(
            {"jsonrpc": "2.0", "id": request.get("id"), "error": {"code": -32601, "message": "unknown method"}},
            status=404,
        )

    def do_GET(self):
        self._record({"method": "GET"})
        self.send_response(405)
        self.send_header("Allow", "POST")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_DELETE(self):
        self._record({"method": "DELETE"})
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()


@pytest.fixture
def mcp_server(monkeypatch):
    from bundles.parallel_search.plugins.web_search import plugin as search_plugin

    server = _MCPFixtureServer()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    server.config_version = search_plugin.CONFIG.VERSION
    monkeypatch.setattr(search_plugin, "MCP_ENDPOINT", f"http://{host}:{port}/mcp")
    monkeypatch.setattr(search_plugin.CONFIG, "PROXY", None)
    try:
        yield server
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def _request(search_queries=None):
    from app.routes.execute import RunToolRequest

    return RunToolRequest(
        bundle_id="parallel_search",
        plugin_id="web_search",
        input_params={
            "objective": "Find the official Python documentation",
            "search_queries": search_queries if search_queries is not None else ["official Python documentation"],
        },
        credentials={},
    )


async def _execute(search_queries=None):
    from app.routes.execute import api_execute

    return await api_execute(_request(search_queries))


def _error_status(response):
    assert response.status == "success"
    return response.data["status"]


def _recorded_call(server):
    return next(item for item in server.requests if item["request"].get("method") == "tools/call")


@pytest.mark.asyncio
async def test_execute_uses_taskingai_caller_and_returns_search_results(mcp_server):
    mcp_server.payload = {
        "search_id": "fixture-search-id",
        "session_id": "provider-session-id",
        "results": [
            {
                "url": "https://docs.python.org/3/",
                "excerpts": ["Official Python documentation."],
                "title": "Python Documentation",
                "publish_date": "2026-08-19",
            }
        ],
        "warnings": [{"code": "partial", "message": "Some sources were unavailable."}],
    }

    response = await _execute(["official Python documentation", "Python language reference"])

    assert response.status == "success"
    assert json.loads(response.data.data["results"]) == [
        {
            "url": "https://docs.python.org/3/",
            "excerpts": ["Official Python documentation."],
            "title": "Python Documentation",
            "publish_date": "2026-08-19",
        }
    ]
    assert json.loads(response.data.data["warnings"]) == mcp_server.payload["warnings"]
    assert "session_id" not in response.data.data
    assert "search_id" not in response.data.data

    call = _recorded_call(mcp_server)["request"]["params"]
    assert call["name"] == "web_search"
    assert call["arguments"] == {
        "objective": "Find the official Python documentation",
        "search_queries": ["official Python documentation", "Python language reference"],
    }
    assert set(call["arguments"]) == {"objective", "search_queries"}

    for request in mcp_server.requests:
        assert request["headers"].get("user-agent") == f"TaskingAI/{mcp_server.config_version}"
        assert "authorization" not in request["headers"]


@pytest.mark.asyncio
async def test_empty_search_results_remain_a_successful_empty_result(mcp_server):
    mcp_server.payload = {"results": [], "warnings": None}

    response = await _execute()

    assert response.status == "success"
    assert json.loads(response.data.data["results"]) == []
    assert json.loads(response.data.data["warnings"]) == []


@pytest.mark.asyncio
async def test_text_only_mcp_result_is_supported(mcp_server):
    mcp_server.text_only = True
    mcp_server.include_output_schema = False
    mcp_server.payload = {
        "results": [{"url": "https://docs.python.org/3/", "excerpts": ["Python docs."]}],
        "warnings": [],
    }

    response = await _execute()

    assert response.status == "success"
    assert json.loads(response.data.data["results"]) == mcp_server.payload["results"]


@pytest.mark.parametrize(
    ("is_error", "payload"),
    [
        (True, {"results": [], "warnings": []}),
        (False, {"results": None, "warnings": []}),
    ],
)
@pytest.mark.asyncio
async def test_provider_errors_and_malformed_results_are_not_empty_successes(mcp_server, is_error, payload):
    mcp_server.is_error = is_error
    mcp_server.payload = payload

    response = await _execute()

    assert _error_status(response) == 500
    assert "results" not in response.data["data"]


@pytest.mark.asyncio
async def test_jsonrpc_errors_are_reported_as_provider_errors(mcp_server):
    mcp_server.jsonrpc_error = True

    response = await _execute()

    assert _error_status(response) == 500
    assert "results" not in response.data["data"]


@pytest.mark.asyncio
async def test_invalid_query_list_is_rejected_before_provider_request(mcp_server):
    response = await _execute([])

    assert _error_status(response) == 422
    assert mcp_server.requests == []


@pytest.mark.asyncio
async def test_fixed_mcp_endpoint_does_not_follow_redirects(mcp_server):
    mcp_server.redirect_initialize = True

    response = await _execute()

    assert _error_status(response) == 500
    assert all(not item["path"].endswith("/redirect-target") for item in mcp_server.requests)
    assert not any(item["request"].get("method") == "tools/call" for item in mcp_server.requests)

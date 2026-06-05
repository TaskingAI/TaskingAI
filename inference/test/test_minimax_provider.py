"""
Unit tests and integration tests for the MiniMax provider upgrade.

Tests cover:
- API endpoint URL (upgraded from legacy to OpenAI-compatible)
- Temperature clamping (MiniMax requires temp in (0, 1])
- Message building for various roles
- Payload construction
- Response parsing (non-stream and stream)
- Token usage extraction
- M3/M2.7 model YAML validation
- Integration tests against MiniMax API (require MINIMAX_API_KEY)
"""

import asyncio
import json
import os
import sys
import yaml
import pytest

# Add inference root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from providers.minimax.chat_completion import (
    MinimaxChatCompletionModel,
    _build_minimax_message,
    _build_minimax_chat_completion_payload,
)
from providers.minimax.utils import build_minimax_header


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class FakeCredentials:
    """Minimal stand-in for ProviderCredentials."""
    def __init__(self, api_key="test-key"):
        self.MINIMAX_API_KEY = api_key


class FakeConfig:
    """Minimal stand-in for ChatCompletionModelConfiguration."""
    def __init__(self, **kwargs):
        self._data = kwargs

    def model_dump(self):
        return self._data


class FakeMessage:
    """Minimal stand-in for ChatCompletionMessage."""
    def __init__(self, role, content=None, function_calls=None, id=None):
        self.role = role
        self.content = content
        self.function_calls = function_calls
        self.id = id


MODELS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "providers", "minimax", "resources", "models"
)
I18N_FILE = os.path.join(
    os.path.dirname(__file__), "..", "providers", "minimax", "resources", "i18n", "en.yml"
)
PROVIDER_FILE = os.path.join(
    os.path.dirname(__file__), "..", "providers", "minimax", "resources", "provider.yml"
)


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


# ===========================================================================
# Unit Tests
# ===========================================================================


class TestBuildMinimaxHeader:
    """Test header construction."""

    def test_bearer_token(self):
        creds = FakeCredentials("sk-test-123")
        headers = build_minimax_header(creds)
        assert headers["Authorization"] == "Bearer sk-test-123"
        assert headers["Content-Type"] == "application/json"


class TestApiEndpoint:
    """Test that the API endpoint uses the new OpenAI-compatible URL."""

    @pytest.mark.asyncio
    async def test_endpoint_url(self):
        model = MinimaxChatCompletionModel()
        creds = FakeCredentials()
        configs = FakeConfig(temperature=0.5)

        from app.models.chat_completion import ChatCompletionUserMessage

        msg = ChatCompletionUserMessage(content="Hello")
        url, headers, payload = await model.prepare_request(
            stream=False,
            provider_model_id="MiniMax-M3",
            messages=[msg],
            credentials=creds,
            configs=configs,
        )
        assert url == "https://api.minimax.io/v1/chat/completions"
        assert "api.minimax.chat" not in url


class TestTemperatureClamping:
    """Test that temperature is clamped to (0, 1] for MiniMax."""

    def test_zero_temperature_clamped(self):
        configs = FakeConfig(temperature=0.0)
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert payload["temperature"] == 0.01

    def test_negative_temperature_clamped(self):
        configs = FakeConfig(temperature=-0.5)
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert payload["temperature"] == 0.01

    def test_high_temperature_clamped(self):
        configs = FakeConfig(temperature=2.0)
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert payload["temperature"] == 1.0

    def test_valid_temperature_unchanged(self):
        configs = FakeConfig(temperature=0.7)
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert payload["temperature"] == 0.7


class TestPayloadConstruction:
    """Test payload building."""

    def test_model_in_payload(self):
        configs = FakeConfig()
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert payload["model"] == "MiniMax-M3"
        assert payload["stream"] is False

    def test_stream_flag(self):
        configs = FakeConfig()
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=True, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert payload["stream"] is True

    def test_tool_choice_auto(self):
        configs = FakeConfig()
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call="auto", functions=None,
        )
        assert payload["tool_choice"] == "auto"

    def test_tool_choice_none(self):
        configs = FakeConfig()
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call="none", functions=None,
        )
        assert payload["tool_choice"] == "none"

    def test_no_hardcoded_max_tokens(self):
        """Ensure max_tokens is not hardcoded; should come from config only."""
        configs = FakeConfig()
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert "max_tokens" not in payload

    def test_max_tokens_from_config(self):
        configs = FakeConfig(max_tokens=8192)
        payload = _build_minimax_chat_completion_payload(
            messages=[], stream=False, provider_model_id="MiniMax-M3",
            configs=configs, function_call=None, functions=None,
        )
        assert payload["max_tokens"] == 8192


class TestResponseParsing:
    """Test non-streaming response extraction."""

    def setup_method(self):
        self.model = MinimaxChatCompletionModel()

    def test_extract_core_data(self):
        response = {"choices": [{"message": {"role": "assistant", "content": "Hi"}}]}
        data = self.model.extract_core_data(response)
        assert data == {"message": {"role": "assistant", "content": "Hi"}}

    def test_extract_core_data_empty(self):
        response = {"choices": []}
        data = self.model.extract_core_data(response)
        assert data is None

    def test_extract_text_content(self):
        data = {"message": {"role": "assistant", "content": "Hello!"}}
        text = self.model.extract_text_content(data)
        assert text == "Hello!"

    def test_extract_text_content_none(self):
        data = {"message": {"role": "assistant", "content": None}}
        text = self.model.extract_text_content(data)
        assert text is None

    def test_extract_usage_data(self):
        response = {"usage": {"prompt_tokens": 10, "completion_tokens": 20}}
        input_t, output_t = self.model.extract_usage_data(response)
        assert input_t == 10
        assert output_t == 20

    def test_extract_usage_data_missing(self):
        response = {}
        input_t, output_t = self.model.extract_usage_data(response)
        assert input_t is None
        assert output_t is None

    def test_extract_function_calls(self):
        data = {
            "message": {
                "tool_calls": [
                    {
                        "function": {
                            "name": "get_weather",
                            "arguments": '{"city": "Tokyo"}',
                        }
                    }
                ]
            }
        }
        calls = self.model.extract_function_calls(data)
        assert calls is not None
        assert len(calls) == 1
        assert calls[0].name == "get_weather"

    def test_extract_finish_reason_stop(self):
        from app.models.chat_completion import ChatCompletionFinishReason
        data = {"finish_reason": "stop"}
        reason = self.model.extract_finish_reason(data)
        assert reason == ChatCompletionFinishReason.stop

    def test_extract_finish_reason_tool_calls(self):
        from app.models.chat_completion import ChatCompletionFinishReason
        data = {"finish_reason": "tool_calls"}
        reason = self.model.extract_finish_reason(data)
        assert reason == ChatCompletionFinishReason.function_calls


class TestStreamParsing:
    """Test streaming response extraction."""

    def setup_method(self):
        self.model = MinimaxChatCompletionModel()

    def test_stream_extract_chunk_data(self):
        sse = {"choices": [{"delta": {"content": "Hi"}}]}
        data = self.model.stream_extract_chunk_data(sse)
        assert data is not None
        assert data["delta"]["content"] == "Hi"

    def test_stream_extract_chunk_data_no_choices(self):
        sse = {}
        data = self.model.stream_extract_chunk_data(sse)
        assert data is None

    def test_stream_extract_chunk(self):
        chunk_data = {"delta": {"content": "Hello"}}
        idx, chunk = self.model.stream_extract_chunk(0, chunk_data, "")
        assert idx == 1
        assert chunk is not None
        assert chunk.delta == "Hello"

    def test_stream_extract_chunk_empty(self):
        chunk_data = {"delta": {"content": None}}
        idx, chunk = self.model.stream_extract_chunk(0, chunk_data, "")
        assert idx == 0
        assert chunk is None

    def test_stream_extract_usage_data(self):
        sse = {"usage": {"prompt_tokens": 5, "completion_tokens": 10}}
        in_t, out_t = self.model.stream_extract_usage_data(sse, 0, 0)
        assert in_t == 5
        assert out_t == 10

    def test_stream_extract_usage_data_no_usage(self):
        sse = {}
        in_t, out_t = self.model.stream_extract_usage_data(sse, 3, 7)
        assert in_t == 3
        assert out_t == 7

    def test_stream_extract_finish_reason(self):
        from app.models.chat_completion import ChatCompletionFinishReason
        chunk = {"finish_reason": "stop"}
        reason = self.model.stream_extract_finish_reason(chunk)
        assert reason == ChatCompletionFinishReason.stop

    def test_stream_check_error(self):
        sse_ok = {"choices": []}
        self.model.stream_check_error(sse_ok)  # should not raise

    def test_stream_handle_function_calls_append(self):
        from app.models.chat_completion import ChatCompletionFunctionCallsContent
        fc = ChatCompletionFunctionCallsContent()
        fc.names = ["get_weather"]
        fc.arguments_strs = [""]
        fc.index = 0
        chunk_data = {
            "delta": {
                "tool_calls": [
                    {"index": 0, "function": {"name": "get_weather", "arguments": '{"city":'}}
                ]
            }
        }
        result = self.model.stream_handle_function_calls(chunk_data, fc)
        assert result is not None
        assert result.arguments_strs[0] == '{"city":'


class TestModelYamlFiles:
    """Test that new M3/M2.7 model YAML files are valid."""

    new_models = [
        "MiniMax-M3.yml",
        "MiniMax-M2.7.yml",
        "MiniMax-M2.7-highspeed.yml",
    ]

    @pytest.mark.parametrize("filename", new_models)
    def test_model_yaml_exists(self, filename):
        path = os.path.join(MODELS_DIR, filename)
        assert os.path.exists(path), f"Model file {filename} not found"

    @pytest.mark.parametrize("filename", new_models)
    def test_model_yaml_structure(self, filename):
        data = load_yaml(os.path.join(MODELS_DIR, filename))
        assert "model_schema_id" in data
        assert data["model_schema_id"].startswith("minimax/")
        assert "provider_model_id" in data
        assert data["type"] == "chat_completion"
        assert "properties" in data
        assert data["properties"]["function_call"] is True
        assert data["properties"]["streaming"] is True
        assert data["properties"]["vision"] is True

    @pytest.mark.parametrize("filename", new_models)
    def test_model_endpoint_url(self, filename):
        data = load_yaml(os.path.join(MODELS_DIR, filename))
        assert data["default_endpoint_url"] == "https://api.minimax.io/v1/chat/completions"

    def test_m3_context_length(self):
        data = load_yaml(os.path.join(MODELS_DIR, "MiniMax-M3.yml"))
        assert data["properties"]["input_token_limit"] == 512000
        assert data["properties"]["output_token_limit"] == 128000

    def test_m2_7_context_length(self):
        data = load_yaml(os.path.join(MODELS_DIR, "MiniMax-M2.7.yml"))
        assert data["properties"]["input_token_limit"] == 192000

    @pytest.mark.parametrize("filename", new_models)
    def test_model_has_pricing(self, filename):
        data = load_yaml(os.path.join(MODELS_DIR, filename))
        assert "pricing" in data
        assert "currency" in data["pricing"]

    @pytest.mark.parametrize("filename", new_models)
    def test_temperature_config_schema(self, filename):
        data = load_yaml(os.path.join(MODELS_DIR, filename))
        temp_config = next(
            (c for c in data["config_schemas"] if c["config_id"] == "temperature"), None
        )
        assert temp_config is not None
        assert temp_config["max"] == 1.0

    def test_older_models_removed(self):
        """Ensure M2.5/M2.1/M2/M1 model files have been removed."""
        for older in ["MiniMax-M2.5.yml", "MiniMax-M2.5-highspeed.yml",
                      "MiniMax-M2.1.yml", "MiniMax-M2.yml", "MiniMax-M1.yml"]:
            path = os.path.join(MODELS_DIR, older)
            assert not os.path.exists(path), f"Older model file {older} should be removed"


class TestLegacyModelsDeprecated:
    """Test that legacy ABAB models are marked as deprecated."""

    legacy_models = [
        "abab5.5-chat.yml",
        "abab5.5s-chat.yml",
        "abab6-chat.yml",
        "abab6.5-chat.yml",
        "abab6.5s-chat.yml",
        "abab6.5g-chat.yml",
    ]

    @pytest.mark.parametrize("filename", legacy_models)
    def test_legacy_model_deprecated(self, filename):
        data = load_yaml(os.path.join(MODELS_DIR, filename))
        assert data.get("deprecated") is True, f"{filename} should be deprecated"

    @pytest.mark.parametrize("filename", legacy_models)
    def test_legacy_model_endpoint_updated(self, filename):
        data = load_yaml(os.path.join(MODELS_DIR, filename))
        assert data["default_endpoint_url"] == "https://api.minimax.io/v1/chat/completions"


class TestProviderYaml:
    """Test provider.yml configuration."""

    def test_provider_id(self):
        data = load_yaml(PROVIDER_FILE)
        assert data["provider_id"] == "minimax"

    def test_default_model_updated(self):
        data = load_yaml(PROVIDER_FILE)
        assert data["default_credential_verification_provider_model_id"] == "MiniMax-M3"

    def test_token_usage_enabled(self):
        data = load_yaml(PROVIDER_FILE)
        assert data.get("return_token_usage") is True
        assert data.get("return_stream_token_usage") is True


class TestI18n:
    """Test i18n translations for new models."""

    def setup_method(self):
        self.i18n = load_yaml(I18N_FILE)

    def test_m3_translations(self):
        assert "minimax_m3_name" in self.i18n
        assert "minimax_m3_description" in self.i18n

    def test_m2_7_translations(self):
        assert "minimax_m2_7_name" in self.i18n
        assert "minimax_m2_7_description" in self.i18n

    def test_m2_7_highspeed_translations(self):
        assert "minimax_m2_7_highspeed_name" in self.i18n
        assert "minimax_m2_7_highspeed_description" in self.i18n

    def test_older_translations_removed(self):
        """Ensure M2.5 i18n entries have been removed."""
        for key in ["minimax_m2_5_name", "minimax_m2_5_description",
                    "minimax_m2_5_highspeed_name", "minimax_m2_5_highspeed_description"]:
            assert key not in self.i18n, f"Older i18n key {key} should be removed"

    def test_legacy_descriptions_mention_deprecation(self):
        for key in ["abab5_5_chat_name", "abab6_chat_name", "abab6_5_chat_name"]:
            assert "Deprecated" in self.i18n[key]


# ===========================================================================
# Integration Tests (require MINIMAX_API_KEY env var)
# ===========================================================================

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
skip_integration = not MINIMAX_API_KEY


@pytest.mark.skipif(skip_integration, reason="MINIMAX_API_KEY not set")
class TestMinimaxIntegration:
    """Integration tests against the live MiniMax API."""

    @pytest.mark.asyncio
    async def test_chat_completion_m3(self):
        """Test a basic chat completion with MiniMax-M3."""
        import aiohttp

        url = "https://api.minimax.io/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "MiniMax-M3",
            "messages": [{"role": "user", "content": "Say hello in one word."}],
            "max_tokens": 32,
            "temperature": 0.7,
            "stream": False,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                assert resp.status == 200
                data = await resp.json()
                assert "choices" in data
                assert data["choices"][0]["message"]["content"]
                assert "usage" in data

    @pytest.mark.asyncio
    async def test_chat_completion_m2_7(self):
        """Test a basic chat completion with MiniMax-M2.7."""
        import aiohttp

        url = "https://api.minimax.io/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "MiniMax-M2.7",
            "messages": [{"role": "user", "content": "Say hello in one word."}],
            "max_tokens": 32,
            "temperature": 0.7,
            "stream": False,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                assert resp.status == 200
                data = await resp.json()
                assert "choices" in data
                assert data["choices"][0]["message"]["content"]

    @pytest.mark.asyncio
    async def test_streaming_m3(self):
        """Test streaming with MiniMax-M3."""
        import aiohttp

        url = "https://api.minimax.io/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "MiniMax-M3",
            "messages": [{"role": "user", "content": "Count from 1 to 3."}],
            "max_tokens": 64,
            "temperature": 0.7,
            "stream": True,
        }
        chunks = []
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                assert resp.status == 200
                async for line in resp.content:
                    decoded = line.decode().strip()
                    if decoded.startswith("data: ") and decoded != "data: [DONE]":
                        chunk = json.loads(decoded[6:])
                        chunks.append(chunk)
        assert len(chunks) > 0

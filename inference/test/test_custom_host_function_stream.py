import asyncio
import json
from contextlib import asynccontextmanager
from importlib import import_module
from types import SimpleNamespace

import pytest

import app.cache
from app.models import (
    ChatCompletionFinishReason,
    ChatCompletionModelConfiguration,
    ChatCompletionUserMessage,
    ProviderCredentials,
)
from providers.custom_host.chat_completion_function_call import CustomHostFunctionCallChatCompletionModel

model_module = import_module("app.models.chat_completion.model")


@pytest.fixture
def run_stream(monkeypatch):
    async def collect(deltas, finish_reason):
        async def event_bytes():
            choices = [{"delta": {"role": "assistant"}, "finish_reason": None}]
            choices.extend({"delta": delta, "finish_reason": None} for delta in deltas)
            choices.append({"delta": {}, "finish_reason": finish_reason})
            for choice in choices:
                yield ("data: " + json.dumps({"choices": [choice]}) + "\n\n").encode()
            yield b"data: [DONE]\n\n"

        @asynccontextmanager
        async def post(url, **kwargs):
            assert url == "https://example.invalid/v1/chat/completions"
            assert kwargs["json"]["stream"] is True
            yield SimpleNamespace(status=200, content=event_bytes())

        @asynccontextmanager
        async def session():
            yield SimpleNamespace(post=post)

        monkeypatch.setattr(model_module.aiohttp, "ClientSession", session)
        monkeypatch.setattr(app.cache, "get_provider", lambda _: SimpleNamespace(return_stream_token_usage=False))
        model = CustomHostFunctionCallChatCompletionModel()
        return [
            event
            async for event in model.chat_completion_stream(
                provider_model_id="test-model",
                messages=[ChatCompletionUserMessage(content="What is the weather in Paris?")],
                credentials=ProviderCredentials(
                    credentials={
                        "CUSTOM_HOST_ENDPOINT_URL": "https://example.invalid/v1/chat/completions",
                        "CUSTOM_HOST_API_KEY": "test-key",
                    }
                ),
                configs=ChatCompletionModelConfiguration(),
                model_schema=SimpleNamespace(provider_id="custom_host"),
            )
        ]

    return lambda deltas, finish_reason="function_call": asyncio.run(collect(deltas, finish_reason))


@pytest.mark.parametrize(
    "function_deltas",
    [
        [{"name": "get_weather", "arguments": ""}, {"arguments": '{"city":'}, {"arguments": '"Paris"}'}],
        [{"name": "get_weather"}, {"arguments": '{"city":"Paris"}'}],
        [{"arguments": '{"city":'}, {"name": "get_weather"}, {"arguments": '"Paris"}'}],
        [{"name": "get_weather", "arguments": None}, {"name": None, "arguments": '{"city":"Paris"}'}],
        [{"name": "get_", "arguments": ""}, {"name": "weather", "arguments": '{"city":"Paris"}'}],
    ],
    ids=["standard", "name-only", "arguments-first", "null-fields", "split-name"],
)
def test_legacy_stream_assembles_function_call(run_stream, function_deltas):
    events = run_stream([{"function_call": delta} for delta in function_deltas])

    assert len(events) == 1
    completion = events[0]
    assert completion.finish_reason == ChatCompletionFinishReason.function_calls
    assert len(completion.message.function_calls) == 1
    call = completion.message.function_calls[0]
    assert call.id
    assert call.name == "get_weather"
    assert call.arguments == {"city": "Paris"}


def test_legacy_stream_keeps_plain_text(run_stream):
    events = run_stream([{"content": "Hello"}, {}, {"content": " world"}], finish_reason="stop")

    assert [event.delta for event in events[:-1]] == ["Hello", " world"]
    assert events[-1].message.content == "Hello world"
    assert events[-1].message.function_calls is None
    assert events[-1].finish_reason == ChatCompletionFinishReason.stop

import asyncio
import json

import pytest
from fastapi import HTTPException

from app.models import (
    ChatCompletionAssistantMessage,
    ChatCompletionFunction,
    ChatCompletionFunctionCall,
    ChatCompletionFunctionMessage,
    ChatCompletionModelConfiguration,
    ChatCompletionSystemMessage,
    ChatCompletionUserMessage,
    ProviderCredentials,
)
from providers.custom_host.chat_completion_function_call import CustomHostFunctionCallChatCompletionModel
from providers.custom_host.chat_completion_tool_calls import CustomHostToolCallsChatCompletionModel


@pytest.fixture
def messages():
    return [
        ChatCompletionSystemMessage(content="Use the search tools."),
        ChatCompletionUserMessage(content="Find papers and their authors."),
        ChatCompletionAssistantMessage(
            function_calls=[
                ChatCompletionFunctionCall(id="call_search", name="arxiv_search", arguments={"q": "agents"})
            ]
        ),
        ChatCompletionFunctionMessage(id="call_search", content="paper-1"),
        ChatCompletionAssistantMessage(
            function_calls=[
                ChatCompletionFunctionCall(id="call_authors", name="get_authors", arguments={"id": "paper-1"})
            ]
        ),
        ChatCompletionFunctionMessage(id="call_authors", content="Author A"),
    ]


def prepare_payload(model, messages, stream):
    credentials = ProviderCredentials(
        credentials={
            "CUSTOM_HOST_ENDPOINT_URL": "https://example.invalid/v1/chat/completions",
            "CUSTOM_HOST_API_KEY": "test-key",
        }
    )
    functions = [
        ChatCompletionFunction(name="arxiv_search", description="Search papers", parameters={"properties": {}})
    ]
    url, headers, payload = asyncio.run(
        model.prepare_request(
            stream=stream,
            provider_model_id="test-model",
            messages=messages,
            credentials=credentials,
            configs=ChatCompletionModelConfiguration(temperature=0.5),
            function_call="auto",
            functions=functions,
        )
    )
    assert url == credentials.CUSTOM_HOST_ENDPOINT_URL
    assert headers["Authorization"] == "Bearer test-key"
    assert payload["model"] == "test-model"
    assert payload["stream"] is stream
    assert payload["temperature"] == 0.5
    return payload


@pytest.mark.parametrize("stream", [False, True])
def test_legacy_function_call_history_uses_function_messages(messages, stream):
    original = [message.model_dump() for message in messages]
    payload = prepare_payload(CustomHostFunctionCallChatCompletionModel(), messages, stream)

    assert "tools" not in payload
    assert payload["function_call"] == "auto"
    assert payload["functions"][0]["name"] == "arxiv_search"
    assert payload["messages"][:2] == [
        {"role": "system", "content": "Use the search tools."},
        {"role": "user", "content": "Find papers and their authors."},
    ]
    for index, name, arguments, result in [
        (2, "arxiv_search", {"q": "agents"}, "paper-1"),
        (4, "get_authors", {"id": "paper-1"}, "Author A"),
    ]:
        assert payload["messages"][index] == {
            "role": "assistant",
            "content": None,
            "function_call": {"name": name, "arguments": json.dumps(arguments)},
        }
        assert payload["messages"][index + 1] == {"role": "function", "name": name, "content": result}
    assert [message.model_dump() for message in messages] == original


@pytest.mark.parametrize("stream", [False, True])
def test_tool_call_history_keeps_tool_messages(messages, stream):
    payload = prepare_payload(CustomHostToolCallsChatCompletionModel(), messages, stream)

    assert "functions" not in payload
    assert payload["tool_choice"] == "auto"
    assert payload["tools"][0]["function"]["name"] == "arxiv_search"
    for index, call_id, name, arguments, result in [
        (2, "call_search", "arxiv_search", {"q": "agents"}, "paper-1"),
        (4, "call_authors", "get_authors", {"id": "paper-1"}, "Author A"),
    ]:
        assert payload["messages"][index] == {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": call_id, "type": "function", "function": {"name": name, "arguments": json.dumps(arguments)}}
            ],
        }
        assert payload["messages"][index + 1] == {"role": "tool", "tool_call_id": call_id, "content": result}


@pytest.mark.parametrize(
    "model_class", [CustomHostFunctionCallChatCompletionModel, CustomHostToolCallsChatCompletionModel]
)
def test_plain_and_multimodal_messages_are_preserved(model_class):
    content = [
        {"type": "text", "text": "Describe this"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,AA=="}},
    ]
    messages = [ChatCompletionUserMessage(content=content), ChatCompletionAssistantMessage(content="A picture.")]
    payload = prepare_payload(model_class(), messages, False)
    assert payload["messages"] == [
        {"role": "user", "content": content},
        {"role": "assistant", "content": "A picture."},
    ]


def test_legacy_function_call_rejects_parallel_calls(messages):
    messages[2].function_calls.append(messages[4].function_calls[0])
    with pytest.raises(HTTPException) as exc_info:
        prepare_payload(CustomHostFunctionCallChatCompletionModel(), messages, False)
    assert exc_info.value.status_code == 422
    assert "openai-tool-calls" in exc_info.value.detail["message"]

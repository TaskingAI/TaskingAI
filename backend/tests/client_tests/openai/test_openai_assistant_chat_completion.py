import pytest
from backend.tests.client_tests.openai import client
from openai.types.chat.chat_completion_chunk import ChoiceDeltaFunctionCall, ChoiceDeltaToolCall
from openai.types.chat.chat_completion_message import FunctionCall
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
import json
from backend.tests.services_tests.assistant import Assistant


@pytest.mark.api_test
class TestOpenAIAssistantChatCompletion(Assistant):
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_017")
    async def test_chat_completion_by_stream(self):
        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=[
                {"role": "user", "content": "Hello, how are you?"},
            ],
            stream=True,
        )
        for chunk in res:
            print(chunk)
            assert chunk.object == "chat.completion.chunk"
            assert len(chunk.choices) == 1
            for choice in chunk.choices:
                assert choice.finish_reason is None, choice
                assert choice.index >= 0, choice
                assert choice.delta.role == "assistant"
                assert choice.delta.content is not None
                assert choice.delta.function_call is None
                assert choice.delta.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_018")
    async def test_chat_completion_by_normal(self):
        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=[
                {"role": "user", "content": "Hello, how are you?"},
            ],
            stream=False,
        )
        assert len(res.choices) == 1
        for choice in res.choices:
            assert choice.finish_reason == "stop", choice
            assert choice.message.role == "assistant"
            assert choice.message.content is not None
            assert choice.message.function_call is None
            assert choice.message.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_019")
    async def test_chat_completion_by_stream_and_function_call(self):
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "add_two_number",
                "description": "Add two number and return sum",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number."},
                        "b": {"type": "number", "description": "Second number."},
                    },
                    "required": ["a", "b"],
                },
            },
        ]
        messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=messages,
            functions=functions,
            function_call="auto",
            stream=True,
        )
        for chunk in res:
            print(chunk)
            assert chunk.object == "chat.completion.chunk"
            assert len(chunk.choices) == 1
            for choice in chunk.choices:
                assert choice.finish_reason == "function_call", choice
                assert choice.index >= 0, choice
                assert choice.delta.role == "assistant"
                assert choice.delta.content is None
                assert isinstance(choice.delta.function_call, ChoiceDeltaFunctionCall)
                assert choice.delta.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_020")
    async def test_chat_completion_by_normal_function_call(self):
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "add_two_number",
                "description": "Add two number and return sum",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number."},
                        "b": {"type": "number", "description": "Second number."},
                    },
                    "required": ["a", "b"],
                },
            },
        ]
        messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=messages,
            functions=functions,
            function_call="auto",
            stream=False,
        )
        assert len(res.choices) == 1
        for choice in res.choices:
            assert choice.finish_reason == "function_call", choice
            assert choice.message.role == "assistant"
            assert choice.message.content is None
            assert isinstance(choice.message.function_call, FunctionCall)
            assert choice.message.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_021")
    async def test_chat_completion_by_stream_function_call_result(self):

        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=[
                {"role": "user", "content": "what is 1324 + 24"},
                {
                    "content": None,
                    "role": "assistant",
                    "function_call": {
                        "id": "P3lf2qkKrmGe08gh8AXHzEyj",
                        "arguments": json.dumps({"a": 1324, "b": 24}),
                        "name": "add_two_number",
                    },
                },
                {"id": "P3lf2qkKrmGe08gh8AXHzEyj", "role": "function", "content": "1348"},
            ],
            stream=True,
        )
        for chunk in res:
            print(chunk)
            assert chunk.object == "chat.completion.chunk"
            assert len(chunk.choices) == 1
            for choice in chunk.choices:
                assert choice.finish_reason is None, choice
                assert choice.index >= 0, choice
                assert choice.delta.role == "assistant"
                assert choice.delta.content is not None
                assert choice.delta.function_call is None
                assert choice.delta.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_022")
    async def test_chat_completion_by_normal_function_call_result(self):

        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=[
                {"role": "user", "content": "what is 1324 + 24"},
                {
                    "content": None,
                    "role": "assistant",
                    "function_call": {
                        "id": "P3lf2qkKrmGe08gh8AXHzEyj",
                        "arguments": json.dumps({"a": 1324, "b": 24}),
                        "name": "add_two_number",
                    },
                },
                {"id": "P3lf2qkKrmGe08gh8AXHzEyj", "role": "function", "content": "1348"},
            ],
            stream=False,
        )
        assert len(res.choices) == 1
        for choice in res.choices:
            assert choice.finish_reason == "stop", choice
            assert choice.message.role == "assistant"
            assert choice.message.content is not None
            assert choice.message.function_call is None
            assert choice.message.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_023")
    async def test_chat_completion_by_stream_and_multi_function_call(self):
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        ]
        messages = [{"role": "user", "content": "What's the weather like in Boston and NewYork today?"}]
        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=messages,
            functions=functions,
            function_call="auto",
            stream=True,
        )
        for chunk in res:
            print(chunk)
            assert chunk.object == "chat.completion.chunk"
            assert len(chunk.choices) == 1
            for choice in chunk.choices:
                assert choice.finish_reason == "function_call", choice
                assert choice.index >= 0, choice
                assert choice.delta.role == "assistant"
                assert choice.delta.content is None
                assert isinstance(choice.delta.function_call, ChoiceDeltaFunctionCall)
                assert choice.delta.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_024")
    async def test_chat_completion_by_stream_and_multi_tool(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "add_two_number",
                    "description": "Add two number and return sum",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number."},
                            "b": {"type": "number", "description": "Second number."},
                        },
                        "required": ["a", "b"],
                    },
                },
            },
        ]

        messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
        res = client.chat.completions.create(
            model=Assistant.assistant_id, messages=messages, tools=tools, tool_choice="auto", stream=True
        )
        for chunk in res:
            print(chunk)
            assert chunk.object == "chat.completion.chunk"
            assert len(chunk.choices) == 1
            for choice in chunk.choices:
                assert choice.finish_reason == "tool_calls", choice
                assert choice.index >= 0, choice
                assert choice.delta.role == "assistant"
                assert choice.delta.content is None
                assert choice.delta.function_call is None
                assert len(choice.delta.tool_calls) == 1
                for tool_call in choice.delta.tool_calls:
                    assert isinstance(tool_call, ChoiceDeltaToolCall)

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_025")
    async def test_chat_completion_by_normal_and_multi_tool(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "add_two_number",
                    "description": "Add two number and return sum",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number."},
                            "b": {"type": "number", "description": "Second number."},
                        },
                        "required": ["a", "b"],
                    },
                },
            },
        ]

        messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
        res = client.chat.completions.create(
            model=Assistant.assistant_id, messages=messages, tools=tools, tool_choice="auto", stream=False
        )

        assert len(res.choices) == 1
        for choice in res.choices:
            assert choice.finish_reason == "tool_calls", choice
            assert choice.index >= 0, choice
            assert choice.message.role == "assistant"
            assert choice.message.content is None
            assert choice.message.function_call is None
            assert len(choice.message.tool_calls) == 1
            for tool_call in choice.message.tool_calls:
                assert isinstance(tool_call, ChatCompletionMessageToolCall)

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_026")
    async def test_chat_completion_by_stream_and_tool_call_result(self):

        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=[
                {"role": "user", "content": "what is 1324 + 24"},
                {
                    "content": None,
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "P3lf0MraPeet2cLjicbWaOxB",
                            "function": {
                                "name": "get_current_weather",
                                "arguments": json.dumps({"location": "Boston, MA"}),
                            },
                            "type": "function",
                        }
                    ],
                },
                {"id": "P3lf0MraPeet2cLjicbWaOxB", "role": "function", "content": "today is sunny"},
            ],
            stream=True,
        )
        for chunk in res:
            print(chunk)
            assert chunk.object == "chat.completion.chunk"
            assert len(chunk.choices) == 1
            for choice in chunk.choices:
                assert choice.finish_reason is None, choice
                assert choice.index >= 0, choice
                assert choice.delta.role == "assistant"
                assert choice.delta.content is not None
                assert choice.delta.function_call is None
                assert choice.delta.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_027")
    async def test_chat_completion_by_normal_and_tool_call_result(self):

        res = client.chat.completions.create(
            model=Assistant.assistant_id,
            messages=[
                {"role": "user", "content": "What's the weather like in Boston today?"},
                {
                    "content": None,
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "P3lf0MraPeet2cLjicbWaOxB",
                            "function": {
                                "name": "get_current_weather",
                                "arguments": json.dumps({"location": "Boston, MA"}),
                            },
                            "type": "function",
                        }
                    ],
                },
                {"id": "P3lf0MraPeet2cLjicbWaOxB", "role": "function", "content": "today is sunny"},
            ],
            stream=False,
        )

        assert len(res.choices) == 1
        for choice in res.choices:
            assert choice.finish_reason == "stop", choice
            assert choice.index >= 0, choice
            assert choice.message.role == "assistant"
            assert choice.message.content is not None
            assert choice.message.function_call is None
            assert choice.message.tool_calls is None

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_028")
    async def test_chat_completion_by_stream_and_multi_tool_call(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "add_two_number",
                    "description": "Add two number and return sum",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number."},
                            "b": {"type": "number", "description": "Second number."},
                        },
                        "required": ["a", "b"],
                    },
                },
            },
        ]

        messages = [{"role": "user", "content": "What's the weather like in Boston and NewYork today?"}]
        res = client.chat.completions.create(
            model=Assistant.assistant_id, messages=messages, tools=tools, tool_choice="auto", stream=True
        )
        for chunk in res:
            print(chunk)
            assert chunk.object == "chat.completion.chunk"
            assert len(chunk.choices) == 1
            for choice in chunk.choices:
                assert choice.finish_reason == "tool_calls", choice
                assert choice.index >= 0, choice
                assert choice.delta.role == "assistant"
                assert choice.delta.content is None
                assert choice.delta.function_call is None
                assert len(choice.delta.tool_calls) >= 1
                for tool_call in choice.delta.tool_calls:
                    assert isinstance(tool_call, ChoiceDeltaToolCall)

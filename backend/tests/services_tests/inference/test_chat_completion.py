import pytest
import asyncio
from backend.tests.common.utils import sse_stream
from backend.tests.common.logger import logger
from backend.tests.api_services.inference.chat_completion import chat_completion
from backend.tests.common.config import CONFIG

INFERENCE_BASE_URL = CONFIG.BASE_URL
CHAT_COMPLETION_URL = f"{INFERENCE_BASE_URL}/inference/chat_completion"


@pytest.mark.api_test
class TestChatCompletion:
    error_configs_list = [
        {
            "temperature": -1.0,
        },
        {
            "temperature": 2.0,
        },
        {
            "temperature": "test",
        },
        {
            "max_tokens": -8192,
        },
        {
            "max_tokens": 81920,
        },
        {
            "max_tokens": "test",
        },
        {
            "top_p": -1.0,
        },
        {
            "top_p": 2.0,
        },
        {
            "top_p": "test",
        },
        {
            "stop": ["*" * 100, "1", "test3", "test4", "test5", "test6"],
        },
        {
            "stop": ["*" * 200],
        },
        {
            "stop": [""],
        },
        {
            "stop": "test",
        },
    ]

    @pytest.mark.run(order=121)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_006")
    async def test_chat_completion_by_normal(self):

        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.togetherai_chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
            CONFIG.fallbacks_debug_error_model_id
        ]

        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "Hello, nice to meet you, what is your name"}],
                "stream": "False",
                "configs": {
                    "temperature": 0.0,
                    "max_tokens": 4096,
                    "top_p": 0.0,
                    "stop": ["you", "me"],
                    "test": "test",
                },
            }

            res = await chat_completion(chat_completion_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("finish_reason") == "stop"
            assert res_json.get("data").get("message").get("role") == "assistant"
            assert res_json.get("data").get("message").get("content") is not None
            assert res_json.get("data").get("message").get("function_calls") is None


    @pytest.mark.run(order=122)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_008")
    @pytest.mark.test_id("inference_010")
    async def test_chat_completion_by_normal_function_call(self):

        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.togetherai_chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
        ]

        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "what is 18794658 + 9731686"}],
                "stream": "False",
                     "configs": {
                    "temperature": 1.0,
                    "max_tokens": 100,
                    "top_p": 1.0,
                    "stop": ["you"],
                    "test": "test",
                },
                "function_call": "auto",
                "functions": [
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
                    }
                ],
            }

            res = await chat_completion(chat_completion_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("finish_reason") == "function_calls"
            assert res_json.get("data").get("message").get("role") == "assistant"
            assert res_json.get("data").get("message").get("content") is None
            assert res_json.get("data").get("message").get("function_calls") is not None

            await asyncio.sleep(1)

    @pytest.mark.run(order=123)
    @pytest.mark.asyncio
    async def test_chat_completion_by_normal_function_call_result(self):

        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.togetherai_chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
            CONFIG.fallbacks_debug_error_model_id
        ]
        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [
                    {"role": "user", "content": "what is 1324 + 24"},
                    {
                        "content": None,
                        "role": "assistant",
                        "function_calls": [
                            {
                                "id": "P3lf2qkKrmGe08gh8AXHzEyj",
                                "arguments": {"a": 1324, "b": 24},
                                "name": "add_two_number",
                            }
                        ],
                    },
                    {"id": "P3lf2qkKrmGe08gh8AXHzEyj", "role": "function", "content": "1348"},
                ],
                "stream": "False",
                "configs": {"temperature": 1.0},
            }

            res = await chat_completion(chat_completion_data)
            res_json = res.json()
            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("finish_reason") == "stop"
            assert res_json.get("data").get("message").get("role") == "assistant"
            assert res_json.get("data").get("message").get("content") is not None
            assert res_json.get("data").get("message").get("function_calls") is None


    @pytest.mark.run(order=124)
    @pytest.mark.asyncio
    async def test_chat_completion_by_normal_length(self):
        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.togetherai_chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
            CONFIG.fallbacks_debug_error_model_id
        ]

        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "Hello, nice to meet you, what is your name"}],
                "stream": "False",
                "configs": {"temperature": 1.0, "max_tokens": 3},
            }

            res = await chat_completion(chat_completion_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("finish_reason") == "length"
            assert res_json.get("data").get("message").get("role") == "assistant"
            assert res_json.get("data").get("message").get("content") is not None
            assert res_json.get("data").get("message").get("function_calls") is None

    @pytest.mark.run(order=125)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_005")
    async def test_chat_completion_by_stream(self):

        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.togetherai_chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
            CONFIG.fallbacks_debug_error_model_id
        ]

        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "Hello, nice to meet you, what is your name"}],
                "stream": "True",
                "configs": {"temperature": 1.0},
            }
            default = False

            async for response_dict in sse_stream(CONFIG.Authentication, CHAT_COMPLETION_URL, chat_completion_data):
                logger.info(response_dict)
                if response_dict.get("object") == "ChatCompletion":
                    assert response_dict.get("finish_reason") == "stop"
                    assert response_dict.get("message").get("role") == "assistant"
                    assert response_dict.get("message").get("content") is not None
                    assert response_dict.get("message").get("function_calls") is None
                    default = True
                elif response_dict.get("object") == "ChatCompletionChunk":
                    assert response_dict.get("role") == "assistant"
                    assert response_dict.get("index") >= 0
                    assert response_dict.get("delta") is not None
                else:
                    assert False, response_dict

            assert default, "stream failed"


    @pytest.mark.run(order=126)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_007")
    @pytest.mark.test_id("inference_009")
    @pytest.mark.test_id("inference_011")
    async def test_chat_completion_by_stream_and_function_call(self):

        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.togetherai_chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
        ]
        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "what is 18794658 + 9731686"}],
                "stream": "True",
                "configs": {"temperature": 1.0},
                "function_call": "auto",
                "functions": [
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
                    }
                ],
            }
            default = False

            async for response_dict in sse_stream(CONFIG.Authentication, CHAT_COMPLETION_URL, chat_completion_data):
                logger.info(response_dict)
                assert response_dict.get("object") == "ChatCompletion"
                assert response_dict.get("finish_reason") == "function_calls"
                assert response_dict.get("message").get("role") == "assistant"
                assert response_dict.get("message").get("content") is None
                assert response_dict.get("message").get("function_calls") is not None
                default = True
            assert default is True

    @pytest.mark.run(order=127)
    @pytest.mark.asyncio
    async def test_chat_completion_by_stream_and_length(self):
        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.togetherai_chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
            CONFIG.fallbacks_debug_error_model_id
        ]

        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "Hello, nice to meet you, what is your name"}],
                "stream": "True",
                "configs": {"temperature": 1.0, "max_tokens": 5},
            }

            default = False

            async for response_dict in sse_stream(CONFIG.Authentication, CHAT_COMPLETION_URL, chat_completion_data):
                logger.info(response_dict)

                if response_dict.get("object") == "ChatCompletion":
                    assert response_dict.get("finish_reason") == "length"
                    assert response_dict.get("message").get("role") == "assistant"
                    assert response_dict.get("message").get("content") is not None
                    assert response_dict.get("message").get("function_calls") is None
                    default = True
                elif response_dict.get("object") == "ChatCompletionChunk":
                    assert response_dict.get("role") == "assistant"
                    assert response_dict.get("index") >= 0
                    assert response_dict.get("delta") is not None
                else:
                    assert False, response_dict
            assert default, "stream failed"

    @pytest.mark.run(order=128)
    @pytest.mark.asyncio
    async def test_chat_completion_by_function_call_and_length(self):
        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
        ]

        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "what is 18794658 + 9731686"}],
                "stream": "False",
                "configs": {"temperature": 1.0, "max_tokens": 1},
                "function_call": "auto",
                "functions": [
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
                    }
                ],
            }

            res = await chat_completion(chat_completion_data)

            assert res.status_code == 400, res.json()
            assert res.json().get("status") == "error"
            assert res.json().get("error").get("code") == "PROVIDER_ERROR"

    @pytest.mark.run(order=129)
    @pytest.mark.asyncio
    async def test_chat_completion_by_stream_and_function_call_and_length(self):
        chat_completion_model_id_list = [
            CONFIG.chat_completion_model_id,
            CONFIG.custom_host_chat_completion_model_id,
            CONFIG.fallbacks_chat_completion_model_id,
        ]

        for model_id in chat_completion_model_id_list:
            chat_completion_data = {
                "model_id": model_id,
                "messages": [{"role": "user", "content": "what is 18794658 + 9731686"}],
                "stream": "True",
                "configs": {"temperature": 1.0, "max_tokens": 3},
                "function_call": "auto",
                "functions": [
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
                    }
                ],
            }

            res = await chat_completion(chat_completion_data)
            assert res.status_code == 400, res.json()
            assert res.json().get("status") == "error"
            assert res.json().get("error").get("code") == "PROVIDER_ERROR"


    @pytest.mark.run(order=130)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.0")
    @pytest.mark.test_id("model_041")
    async def test_chat_completion_by_not_support_stream(self):

        chat_completion_data = {
            "model_id": CONFIG.not_stream_wildcard_chat_completion_model_id,
            "messages": [{"role": "user", "content": "Hello, nice to meet you, what is your name"}],
            "stream": "True",
            "configs": {"temperature": 1.0},
        }

        res = await chat_completion(chat_completion_data)
        res_json = res.json()

        pytest.assume(res.status_code == 422, res.json())
        pytest.assume(res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR")

    @pytest.mark.run(order=130)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("model_045")
    @pytest.mark.parametrize("configs", error_configs_list)
    async def test_chat_completion_by_error_configs(self, configs):
        chat_completion_data = {
            "model_id": CONFIG.chat_completion_model_id,
            "messages": [{"role": "user", "content": "Hello, nice to meet you, what is your name"}],
            "stream": "False",
            "configs": configs,
            "function_call": "auto",
            "functions": [
                {
                    "name": "make_scatter_plot",
                    "description": "Generate a scatter plot from the given data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x_values": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "The x-axis values for the data points",
                            },
                            "y_values": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "The y-axis values for the data points",
                            },
                        },
                        "required": ["x_values", "y_values"],
                    },
                }
            ],
        }
        res = await chat_completion(chat_completion_data)
        res_json = res.json()
        pytest.assume(res.status_code == 422, res.json())
        pytest.assume(res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR", res_json)

import pytest

from backend.tests.common.utils import sse_stream
from backend.tests.services_tests.assistant import Assistant
from backend.tests.api_services.inference.chat_completion import chat_completion
from backend.tests.common.config import CONFIG


INFERENCE_BASE_URL = CONFIG.BASE_URL
CHAT_COMPLETION_URL = f"{INFERENCE_BASE_URL}/inference/chat_completion"


@pytest.mark.api_test
class TestAssistantChatCompletion(Assistant):

    except_dict = {"except_http_code": "200", "except_status": "success"}
    error_dict = {"except_http_code": "500", "except_status": "error", "except_error_code": "GENERATION_ERROR"}

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_013")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_sample_chat_completion(self):


        chat_completion_dict = {
            "model_id": Assistant.assistant_ids[0],
            "messages": [
                {"role": "system", "content": "Now it is 2025"},
                {"role": "user", "content": "what is Fingerbot"},
                {
                    "role": "assistant",
                    "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                },
                {"role": "user", "content": "wow, Thank you!"},
                {
                    "role": "assistant",
                    "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                },
                {"role": "user", "content": "what is 18 + 20?"},
            ],
            "stream": False,
            "save_logs": False,
        }
        res = await chat_completion(chat_completion_dict)
        assert res.status_code == 200, res.json()
        assert res.json().get("status") == "success"
        res_data = res.json().get("data")
        assert res_data.get("finish_reason") == "stop"
        assert res_data.get("message").get("role") == "assistant"
        assert res_data.get("message").get("content") is not None
        assert res_data.get("message").get("function_calls") is None

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_012")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_sample_chat_completion_by_stream(self):


        chat_completion_dict = {
            "model_id": Assistant.assistant_ids[0],
            "messages": [
                {"role": "system", "content": "Now it is 2025"},
                {"role": "user", "content": "what is Fingerbot"},
                {
                    "role": "assistant",
                    "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                },
                {"role": "user", "content": "wow, Thank you!"},
                {
                    "role": "assistant",
                    "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                },
                {"role": "user", "content": "what is 18 + 20?"},
            ],
            "stream": True,
            "save_logs": False,
        }
        default = False

        async for response_dict in sse_stream(CONFIG.Authentication, CHAT_COMPLETION_URL, chat_completion_dict):

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

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_015")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_sample_chat_completion_by_function(self):

            chat_completion_dict = {
                "model_id": Assistant.assistant_ids[0],
                "messages": [
                    {"role": "system", "content": "Now it is 2025"},
                    {"role": "user", "content": "what is Fingerbot"},
                    {
                        "role": "assistant",
                        "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                    },
                    {"role": "user", "content": "wow, Thank you!"},
                    {
                        "role": "assistant",
                        "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                    },
                    {"role": "user", "content": "what is 497956549 + 6898498491?"},
                ],
                "stream": False,
                "save_logs": False,
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
            res = await chat_completion(chat_completion_dict)
            assert res.status_code == 200, res.json()
            assert res.json().get("status") == "success"
            res_data = res.json().get("data")
            assert res_data.get("finish_reason") == "function_calls"
            assert res_data.get("message").get("role") == "assistant"
            assert res_data.get("message").get("content") is None
            assert res_data.get("message").get("function_calls") is not None

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_014")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_sample_chat_completion_by_stream_and_function(self):

            chat_completion_dict = {
                "model_id": Assistant.assistant_ids[0],
                "messages": [
                    {"role": "system", "content": "Now it is 2025"},
                    {"role": "user", "content": "what is Fingerbot"},
                    {
                        "role": "assistant",
                        "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                    },
                    {"role": "user", "content": "wow, Thank you!"},
                    {
                        "role": "assistant",
                        "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                    },
                    {"role": "user", "content": "what is 497956549 + 6898498491?"},
                ],
                "stream": True,
                "save_logs": False,
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
            async for response_dict in sse_stream(CONFIG.Authentication, CHAT_COMPLETION_URL, chat_completion_dict):
                default = True
                assert response_dict.get("object") == "ChatCompletion"
                assert response_dict.get("finish_reason") == "function_calls"
                assert response_dict.get("message").get("role") == "assistant"
                assert response_dict.get("message").get("content") is None
                assert response_dict.get("message").get("function_calls") is not None
            assert default is True

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_017")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_complex_chat_completion(self):


        chat_completion_dict = {
            "model_id": Assistant.assistant_ids[1],
            "messages": [
                {"role": "system", "content": "Now it is 2025"},
                {"role": "user", "content": "what is Fingerbot"},
                {
                    "role": "assistant",
                    "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                },
                {"role": "user", "content": "wow, Thank you!"},
                {
                    "role": "assistant",
                    "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                },
                {"role": "user", "content": "what is 18 + 20?"},
            ],
            "stream": False,
            "save_logs": False,
        }
        res = await chat_completion(chat_completion_dict)
        assert res.status_code == 200, res.json()
        assert res.json().get("status") == "success"
        res_data = res.json().get("data")
        assert res_data.get("finish_reason") == "stop"
        assert res_data.get("message").get("role") == "assistant"
        assert res_data.get("message").get("content") is not None
        assert res_data.get("message").get("function_calls") is None

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_016")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_complex_chat_completion_by_stream(self):


        chat_completion_dict = {
            "model_id": Assistant.assistant_ids[1],
            "messages": [
                {"role": "system", "content": "Now it is 2025"},
                {"role": "user", "content": "what is Fingerbot"},
                {
                    "role": "assistant",
                    "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                },
                {"role": "user", "content": "wow, Thank you!"},
                {
                    "role": "assistant",
                    "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                },
                {"role": "user", "content": "what is 18 + 20?"},
            ],
            "stream": True,
            "save_logs": False,
        }
        default = False

        async for response_dict in sse_stream(CONFIG.Authentication, CHAT_COMPLETION_URL, chat_completion_dict):

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

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_019")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_complex_chat_completion_by_function(self):


        chat_completion_dict = {
            "model_id": Assistant.assistant_ids[1],
            "messages": [
                {"role": "system", "content": "Now it is 2025"},
                {"role": "user", "content": "what is Fingerbot"},
                {
                    "role": "assistant",
                    "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                },
                {"role": "user", "content": "wow, Thank you!"},
                {
                    "role": "assistant",
                    "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                },
                {"role": "user", "content": "what is 497956549 + 6898498491?"},
            ],
            "stream": False,
            "save_logs": False,
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
        res = await chat_completion(chat_completion_dict)
        assert res.status_code == 200, res.json()
        assert res.json().get("status") == "success"
        res_data = res.json().get("data")
        assert res_data.get("finish_reason") == "function_calls"
        assert res_data.get("message").get("role") == "assistant"
        assert res_data.get("message").get("content") is None
        assert res_data.get("message").get("function_calls") is not None

    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_018")
    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_openai_complex_chat_completion_by_stream_and_function(self):

        chat_completion_dict = {
            "model_id": Assistant.assistant_ids[1],
            "messages": [
                {"role": "system", "content": "Now it is 2025"},
                {"role": "user", "content": "what is Fingerbot"},
                {
                    "role": "assistant",
                    "content": "Fingerbot is the world's smallest robot designed to smartly control different types of buttons and switches. It allows you to automate and control your existing home appliances with robotic clicks. With Fingerbot, you can switch lights via an app, schedule tasks like making a morning coffee, activate devices with voice commands, and remotely power on electronics like your office PC. The device offers convenience and automation in managing various devices around your home or workspace.",
                },
                {"role": "user", "content": "wow, Thank you!"},
                {
                    "role": "assistant",
                    "content": "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!",
                },
                {"role": "user", "content": "what is 497956549 + 6898498491?"},
            ],
            "stream": True,
            "save_logs": False,
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

        async for response_dict in sse_stream(CONFIG.Authentication, CHAT_COMPLETION_URL, chat_completion_dict):
            default = True
            assert response_dict.get("object") == "ChatCompletion"
            assert response_dict.get("finish_reason") == "function_calls"
            assert response_dict.get("message").get("role") == "assistant"
            assert response_dict.get("message").get("content") is None
            assert response_dict.get("message").get("function_calls") is not None
        assert default, "stream failed"

import pytest

from tests.services_api.inference.chat_completion import chat_completion
from tests.services_api.model.model import create_model


class TestChatCompletion:

    chat_completion_model_id = None

    @pytest.mark.run(order=31)
    @pytest.mark.asyncio
    async def test_chat_completion_by_normal(self):

        create_chat_completion_model_data = {
            "model_schema_id": "openai/gpt-3.5-turbo",
            "name": "My Language Model",
            "credentials": {"OPENAI_API_KEY": "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"}
        }

        create_chat_completion_model_res = await create_model(create_chat_completion_model_data)
        create_chat_completion_model_res_json = create_chat_completion_model_res.json()
        TestChatCompletion.chat_completion_model_id = create_chat_completion_model_res_json.get("data").get("model_id")

        chat_completion_data = {
                                "model_id": self.chat_completion_model_id,
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": "Hello, nice to meet you, what is your name"
                                    }
                                ],
                                "stream": "False",
                                "configs": {
                                    "temperature": 1.0
                                }
                            }

        res = await chat_completion(chat_completion_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "stop"
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is not None
        assert res_json.get("data").get("message").get("function_calls") is None

    @pytest.mark.run(order=32)
    @pytest.mark.asyncio
    async def test_chat_completion_by_normal_function_call(self):

        chat_completion_data = {
                                "model_id": self.chat_completion_model_id,
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": "what is 1324 + 24"
                                    }
                                ],
                                "stream": "False",
                                "configs": {
                                    "temperature": 1.0
                                },
                                "function_call": "auto",
                                "functions": [
                                    {
                                        "name": "add_two_number",
                                        "description": "Add two number and return sum",
                                        "parameters": {
                                            "type": "object",
                                            "properties": {
                                                "a": {
                                                    "type": "number",
                                                    "description": "First number."
                                                },
                                                "b": {
                                                    "type": "number",
                                                    "description": "Second number."
                                                }
                                            },
                                            "required": ["a", "b"]
                                        }
                                    }
                                ]

                            }

        res = await chat_completion(chat_completion_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "function_calls"
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is None
        assert res_json.get("data").get("message").get("function_calls") is not None

    @pytest.mark.run(order=33)
    @pytest.mark.asyncio
    async def test_chat_completion_by_normal_function_call_result(self):

        chat_completion_data = {
                                "model_id": self.chat_completion_model_id,
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": "what is 1324 + 24"
                                    },
                                    {
                                        "content": None,
                                        "role": "assistant",
                                        "function_calls": [
                                            {
                                                "id": "P3lf2qkKrmGe08gh8AXHzEyj",
                                                "arguments": {
                                                    "a": 1324,
                                                    "b": 24
                                                },
                                                "name": "add_two_number"
                                            }
                                        ]
                                    },
                                    {
                                        "id": "P3lf2qkKrmGe08gh8AXHzEyj",
                                        "role": "function",
                                        "content": "1348"
                                    }
                                ],
                                "stream": "False",
                                "configs": {
                                    "temperature": 1.0
                                }
                            }

        res = await chat_completion(chat_completion_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "stop"
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is not None
        assert res_json.get("data").get("message").get("function_calls") is None

    @pytest.mark.run(order=34)
    @pytest.mark.asyncio
    async def test_chat_completion_by_normal_length(self):

        chat_completion_data = {
            "model_id": self.chat_completion_model_id,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, nice to meet you, what is your name"
                }
            ],
            "stream": "False",
            "configs": {
                "temperature": 1.0,
                "max_tokens": 10
            }
        }

        res = await chat_completion(chat_completion_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "length"
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is not None
        assert res_json.get("data").get("message").get("function_calls") is None

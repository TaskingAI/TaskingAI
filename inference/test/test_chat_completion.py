import allure
import pytest
import asyncio
from test.utils.utils import sse_stream
from test.setting import Config
from test.inference_service.inference import chat_completion
from .utils.utils import generate_test_cases, generate_wildcard_test_cases, is_provider_service_error


@allure.epic("inference_service")
@allure.feature("chat_completion")
class TestChatCompletion:
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_001")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_normal(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = [{"role": "user", "content": "Hello, nice to meet you, what is your name"}]
        if "debug-error" in model_schema_id or "azure" in model_schema_id or "hugging_face" in model_schema_id:
            pytest.skip("Skip the test case with debug-error.")
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": False,
            "configs": configs,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})
        try:
            res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip("Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res_json.get("error").get("message")
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "stop"
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is not None
        assert res_json.get("data").get("message").get("function_calls") is None

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_002")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_normal_function_call(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = test_data["message"]
        function_call = test_data["function_call"]

        if not function_call or "azure" in model_schema_id:
            pytest.skip("Skip the test case without function call.")
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
        }
        functions = test_data["functions"]
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": False,
            "configs": configs,
            "functions": functions,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})
        try:
            res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip("Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "function_calls"
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is None
        assert res_json.get("data").get("message").get("function_calls") is not None

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_003")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_normal_function_call_result(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        function_call = test_data["function_call"]
        if not function_call or "debug-error" in model_schema_id or "azure" in model_schema_id:
            pytest.skip("Skip the test case without function call or debug-error")
        message = test_data["message"]
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": False,
            "configs": configs,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})
        try:
            res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip("Skip the test case with provider service error.")
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "stop", res_json
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is not None
        assert res_json.get("data").get("message").get("function_calls") is None

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_004")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_normal_length(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        if (
            "debug" in model_schema_id
            or "google_gemini" in model_schema_id
            or "hugging_face" in model_schema_id
            or "sensetime" in model_schema_id
        ):
            # google_gemini model response is empty
            pytest.skip("Skip the test case.")
        message = [{"role": "user", "content": "introduce yourself in detail"}]
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
            "max_tokens": 2,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": False,
            "configs": configs,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})

        try:
            res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip("Skip the test case with provider service error.")
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("finish_reason") == "length"
        assert res_json.get("data").get("message").get("role") == "assistant"
        assert res_json.get("data").get("message").get("content") is not None
        assert res_json.get("data").get("message").get("function_calls") is None

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_005")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_stream(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = test_data["message"]
        stream = test_data["stream"]
        function_call = test_data["function_call"]
        functions = test_data.get("functions")
        if not stream or "debug" in model_schema_id or "azure" in model_schema_id or function_call or functions:
            pytest.skip("Skip the test case without stream.")
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": True,
            "configs": configs,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})

        request_url = f"{Config.BASE_URL}/chat_completion"

        async for response_dict in sse_stream(request_url, request_data):
            if response_dict.get("object") == "ChatCompletion":
                assert response_dict.get("finish_reason") == "stop"
                assert response_dict.get("message").get("role") == "assistant"
                assert response_dict.get("message").get("content") is not None
                assert response_dict.get("message").get("function_calls") is None
            elif response_dict.get("object") == "ChatCompletionChunk":
                assert response_dict.get("role") == "assistant"
                assert response_dict.get("index") >= 0
                assert response_dict.get("delta") is not None
            else:
                assert False, f"response_dict={response_dict}"

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_006")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_stream_and_function_call(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = test_data["message"]
        function_call = test_data["function_call"]
        stream = test_data["stream"]
        if not function_call or not stream or "azure" in model_schema_id:
            pytest.skip("Skip the test case without function call or stream.")
        functions = test_data["functions"]
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": True,
            "configs": configs,
            "functions": functions,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})
        request_url = f"{Config.BASE_URL}/chat_completion"

        async for response_dict in sse_stream(request_url, request_data):
            assert response_dict.get("object") == "ChatCompletion"
            assert response_dict.get("finish_reason") == "function_calls"
            assert response_dict.get("message").get("role") == "assistant"
            assert response_dict.get("message").get("content") is None
            assert response_dict.get("message").get("function_calls") is not None

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_007")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_stream_and_length(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = [{"role": "user", "content": "Hello, nice to meet you, what is your name"}]
        stream = test_data["stream"]
        if (
            not stream
            or "debug" in model_schema_id
            or "minimax/abab5.5s" in model_schema_id
            or "google_gemini" in model_schema_id
            or "sensetime" in model_schema_id
        ):
            pytest.skip("Skip the test case without stream.")
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
            "max_tokens": 10,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": True,
            "configs": configs,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})
        request_url = f"{Config.BASE_URL}/chat_completion"
        except_object = ["ChatCompletionChunk", "ChatCompletion"]
        response_object = []
        async for response_dict in sse_stream(request_url, request_data):
            response_object.append(response_dict.get("object"))
            assert response_dict.get("object") in except_object, f"response_dict={response_dict}"
            if response_dict.get("object") == "ChatCompletion":
                assert response_dict.get("finish_reason") == "length"
                assert response_dict.get("message").get("role") == "assistant"
                assert response_dict.get("message").get("content") is not None
                assert response_dict.get("message").get("function_calls") is None
            if response_dict.get("object") == "ChatCompletionChunk":
                assert response_dict.get("role") == "assistant"
                assert response_dict.get("index") >= 0
                assert response_dict.get("delta") is not None

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_008")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_function_call_and_length(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = test_data["message"]
        function_call = test_data["function_call"]
        if not function_call or "sensetime" in model_schema_id:
            pytest.skip("Skip the test case without function call.")

        functions = test_data["functions"]
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
            "max_tokens": 3,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": False,
            "configs": configs,
            "functions": functions,
        }
        if "wildcard" in model_schema_id:
            request_data.update({"provider_model_id": test_data["provider_model_id"]})
        try:
            res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip("Skip the test case with provider service error.")
        if (
            "mistralai" in model_schema_id
            or "anthropic" in model_schema_id
            or "togetherai" in model_schema_id
            or "google_gemini" in model_schema_id
        ):
            assert res.status_code == 200, res.json()
            assert res.json().get("status") == "success"
            assert res.json().get("data").get("finish_reason") == "length"
            assert res.json().get("data").get("message").get("role") == "assistant"
            assert res.json().get("data").get("message").get("content") is not None
            assert res.json().get("data").get("message").get("function_calls") is None
        else:
            assert res.status_code == 400, res.json()
            assert res.json().get("status") == "error"
            assert res.json().get("error").get("code") == "PROVIDER_ERROR"

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_009")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_stream_and_function_call_and_length(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = test_data["message"]
        function_call = test_data["function_call"]
        stream = test_data["stream"]
        if (
            not function_call
            or not stream
            or "azure" in model_schema_id
            or "mistralai" in model_schema_id
            or "google_gemini" in model_schema_id
            or "sensetime" in model_schema_id
        ):
            pytest.skip("Skip the test case without function call or stream.")
        functions = test_data["functions"]
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
            "max_tokens": 3,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": True,
            "configs": configs,
            "functions": functions,
        }
        if "openai" in model_schema_id or "togetherai" in model_schema_id or "minimax" in model_schema_id:
            request_url = f"{Config.BASE_URL}/chat_completion"
            async for response_dict in sse_stream(request_url, request_data):
                assert response_dict.get("object") == "Error"
                assert response_dict.get("code") == "PROVIDER_ERROR"
        else:
            try:
                res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
            except asyncio.TimeoutError:
                pytest.skip("Skipping test due to timeout after 2 minutes.")
            if is_provider_service_error(res):
                pytest.skip("Skip the test case with provider service error.")
            res_json = res.json()
            assert res.status_code == 400, res.json()
            assert res_json.get("status") == "error"
            assert res_json.get("error").get("code") == "PROVIDER_ERROR"

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_010")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    async def test_chat_completion_by_not_support_stream(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        message = "hello, can you help me?"
        stream = test_data["stream"]
        if stream:
            pytest.skip("Skip the test case with stream.")
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": True,
            "configs": configs,
        }
        try:
            res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip("Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("chat_completion") + generate_wildcard_test_cases("chat_completion"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.parametrize("provider_url", Config.PROVIDER_URL_BLACK_LIST)
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_029")
    async def test_chat_completion_with_error_provider_url(self, test_data, provider_url):
        model_schema_id = test_data["model_schema_id"]
        if "custom_host" not in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        message = test_data["message"]
        configs = {
            "temperature": 0.5,
            "top_p": 0.5,
        }
        request_data = {
            "model_schema_id": model_schema_id,
            "messages": message,
            "stream": False,
            "configs": configs,
        }
        request_data.update(
            {
                "credentials": {
                    "CUSTOM_HOST_ENDPOINT_URL": provider_url,
                    "CUSTOM_HOST_MODEL_ID": "gpt-3.5-turbo",
                    "CUSTOM_HOST_API_KEY": Config.CUSTOM_HOST_API_KEY,
                }
            }
        )
        try:
            res = await asyncio.wait_for(chat_completion(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip("Skip the test case with provider service error.")
        assert res.status_code == 422, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"

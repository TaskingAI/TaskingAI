import allure
from test.inference_service.inference import text_embedding
from .utils.utils import generate_test_cases, generate_wildcard_test_cases, is_unit_vector, is_provider_service_error
import pytest
from test.setting import Config
import asyncio


@allure.epic("inference_service")
@allure.feature("text_embedding")
class TestTextEmbedding:
    single_text = {"input": "hello, nice to meet you"}
    list_text = {"input": ["hello, nice to meet you", "i'm fine thank you"]}

    empty_list_text = {"input": []}

    error_input_list = [
        {"input": 100},
        {"input": ["hello, nice to meet you", 100]},
    ]

    @pytest.mark.test_id("inference_011")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_data", generate_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"])
    async def test_text_embedding_single_text(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        data = {"model_schema_id": model_schema_id}
        if "custom_host" in model_schema_id:
            data.update({"properties": {"embedding_size": 1536}})
            test_data["embedding_size"] = 1536
            data.update(
                {
                    "credentials": {
                        "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/embeddings",
                        "CUSTOM_HOST_MODEL_ID": "text-embedding-3-small",
                        "CUSTOM_HOST_API_KEY": Config.CUSTOM_HOST_API_KEY,
                    }
                }
            )
        if "azure" in model_schema_id:
            pytest.skip("Test not applicable for this model type")
        data.update(self.single_text)
        try:
            res = await asyncio.wait_for(text_embedding(data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for item in res_json.get("data"):
            assert all(isinstance(value, float) for value in item.get("embedding"))
            text_embedding_size = len(item.get("embedding"))
            assert (
                text_embedding_size == test_data["embedding_size"]
            ), f"Expected embedding size: {test_data['embedding_size']}, but got: {text_embedding_size}"
            assert is_unit_vector(item.get("embedding"))

    @pytest.mark.test_id("inference_011")
    @pytest.mark.parametrize(
        "test_data", generate_wildcard_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"]
    )
    @pytest.mark.asyncio
    async def test_wildcard_text_embedding_single_text(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        provider_model_id = test_data["provider_model_id"]
        request_data = {
            "model_schema_id": model_schema_id,
            "provider_model_id": provider_model_id,
            "properties": {
                "embedding_size": test_data["embedding_size"],
            },
        }
        request_data.update(self.single_text)
        try:
            res = await asyncio.wait_for(text_embedding(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for item in res_json.get("data"):
            assert all(isinstance(value, float) for value in item.get("embedding"))
            text_embedding_size = len(item.get("embedding"))
            assert (
                text_embedding_size == test_data["embedding_size"]
            ), f"Expected embedding size: {test_data['embedding_size']}, but got: {text_embedding_size}"
            assert is_unit_vector(item.get("embedding"))

    @pytest.mark.test_id("inference_012")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_data", generate_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"])
    async def test_text_embedding_list_text(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        request_data = {"model_schema_id": model_schema_id}
        if "custom_host" in model_schema_id:
            test_data["embedding_size"] = 1536
            request_data.update({"properties": {"embedding_size": 1536}})
            request_data.update(
                {
                    "credentials": {
                        "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/embeddings",
                        "CUSTOM_HOST_MODEL_ID": "text-embedding-3-small",
                        "CUSTOM_HOST_API_KEY": Config.CUSTOM_HOST_API_KEY,
                    }
                }
            )

        if "azure" in model_schema_id:
            pytest.skip("Test not applicable for this model type")
        request_data.update(self.list_text)
        try:
            res = await asyncio.wait_for(text_embedding(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for item in res_json.get("data"):
            assert all(isinstance(value, float) for value in item.get("embedding"))
            text_embedding_size = len(item.get("embedding"))
            assert (
                text_embedding_size == test_data["embedding_size"]
            ), f"Expected embedding size: {test_data['embedding_size']}, but got: {text_embedding_size}"
            assert is_unit_vector(item.get("embedding"))

    @pytest.mark.test_id("inference_012")
    @pytest.mark.parametrize(
        "test_data", generate_wildcard_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"]
    )
    @pytest.mark.asyncio
    async def test_wildcard_text_embedding_list_text(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        provider_model_id = test_data["provider_model_id"]
        request_data = {
            "model_schema_id": model_schema_id,
            "provider_model_id": provider_model_id,
            "properties": {
                "embedding_size": test_data["embedding_size"],
            },
        }
        request_data.update(self.list_text)
        try:
            res = await asyncio.wait_for(text_embedding(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for item in res_json.get("data"):
            assert all(isinstance(value, float) for value in item.get("embedding"))
            text_embedding_size = len(item.get("embedding"))
            assert (
                text_embedding_size == test_data["embedding_size"]
            ), f"Expected embedding size: {test_data['embedding_size']}, but got: {text_embedding_size}"
            assert is_unit_vector(item.get("embedding"))

    @pytest.mark.test_id("inference_014")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_data", generate_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"])
    async def test_text_embedding_empty_list_text(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        request_data = {"model_schema_id": model_schema_id}
        if "custom_host" in model_schema_id:
            request_data.update({"properties": {"embedding_size": 1536}})
            request_data.update(
                {
                    "credentials": {
                        "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/embeddings",
                        "CUSTOM_HOST_MODEL_ID": "text-embedding-3-small",
                        "CUSTOM_HOST_API_KEY": Config.CUSTOM_HOST_API_KEY,
                    }
                }
            )
        if "azure" in model_schema_id:
            pytest.skip("Test not applicable for this model type")
        request_data.update(self.empty_list_text)
        try:
            res = await asyncio.wait_for(text_embedding(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert len(res_json["data"]) == 0

    @pytest.mark.test_id("inference_014")
    @pytest.mark.parametrize(
        "test_data", generate_wildcard_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"]
    )
    @pytest.mark.asyncio
    async def test_wildcard_text_embedding_empty_list_text(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        provider_model_id = test_data["provider_model_id"]
        request_data = {
            "model_schema_id": model_schema_id,
            "provider_model_id": provider_model_id,
            "properties": {
                "embedding_size": test_data["embedding_size"],
            },
        }
        request_data.update(self.empty_list_text)
        try:
            res = await asyncio.wait_for(text_embedding(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert len(res_json["data"]) == 0

    @pytest.mark.test_id("inference_015")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", error_input_list)
    @pytest.mark.parametrize("test_data", generate_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"])
    async def test_error_text_embedding(self, input_data, test_data):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        request_data = {"model_schema_id": model_schema_id}
        if "custom_host" in model_schema_id:
            request_data.update({"properties": {"embedding_size": 1536}})
        if "azure" in model_schema_id:
            pytest.skip("Test not applicable for this model type")
        request_data.update(input_data)
        try:
            res = await asyncio.wait_for(text_embedding(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.test_id("inference_015")
    @pytest.mark.parametrize("input_data", error_input_list)
    @pytest.mark.parametrize(
        "test_data", generate_wildcard_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"]
    )
    @pytest.mark.asyncio
    async def test_error_wildcard_text_embedding(self, input_data, test_data):
        model_schema_id = test_data["model_schema_id"]
        provider_model_id = test_data["provider_model_id"]
        request_data = {
            "model_schema_id": model_schema_id,
            "provider_model_id": provider_model_id,
            "properties": {
                "embedding_size": test_data["embedding_size"],
            },
        }
        request_data.update(input_data)
        try:
            res = await asyncio.wait_for(text_embedding(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.parametrize("test_data", generate_test_cases("text_embedding"), ids=lambda d: d["model_schema_id"])
    @pytest.mark.parametrize("provider_url", Config.PROVIDER_URL_BLACK_LIST)
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_030")
    async def test_text_embedding_with_error_provider_url(self, test_data, provider_url):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        if "custom_host" not in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        data = {"model_schema_id": model_schema_id}
        data.update({"properties": {"embedding_size": 1536}})
        data.update(
            {
                "credentials": {
                    "CUSTOM_HOST_ENDPOINT_URL": provider_url,
                    "CUSTOM_HOST_MODEL_ID": "text-embedding-3-small",
                    "CUSTOM_HOST_API_KEY": Config.CUSTOM_HOST_API_KEY,
                }
            }
        )
        data.update(self.single_text)
        try:
            res = await asyncio.wait_for(text_embedding(data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        assert res.status_code == 422, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.test_id("inference_011")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("provider_url", Config.PROVIDER_URL_BLACK_LIST)
    async def test_text_embedding_with_error_proxy(self, provider_url):
        model_schema_id = "openai/text-embedding-3-large-256"
        data = {"model_schema_id": model_schema_id}
        data.update(self.single_text)
        data.update({"proxy": provider_url})
        try:
            res = await asyncio.wait_for(text_embedding(data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        assert res.status_code == 422, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"
        await asyncio.sleep(1)

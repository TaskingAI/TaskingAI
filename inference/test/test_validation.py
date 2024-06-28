from test.utils.utils import generate_test_cases_for_validation, generate_wildcard_test_case_for_validation
from test.inference_service.inference import verify_credentials
from app.models import provider_credentials
import pytest
import asyncio
from test.setting import Config


class TestValidation:
    @pytest.mark.parametrize("test_data", generate_test_cases_for_validation(), ids=lambda d: d["model_schema_id"])
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_016-017")
    async def test_validation(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        model_type = test_data["model_type"]

        credentials = {
            key: provider_credentials.aes_decrypt(test_data["credentials"][key])
            for key in test_data["credentials"].keys()
        }

        request_data = {"model_schema_id": model_schema_id, "model_type": model_type, "credentials": credentials}
        if "custom_host" in model_schema_id:
            request_data.update(
                {
                    "model_schema_id": "custom_host/openai-text-embedding",
                    "model_type": "text_embedding",
                    "credentials": {
                        "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/embeddings",
                        "CUSTOM_HOST_MODEL_ID": "text-embedding-3-small",
                        "CUSTOM_HOST_API_KEY": Config.CUSTOM_HOST_API_KEY,
                    },
                    "properties": {"embedding_size": 1536},
                }
            )
        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 200, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "success", f"test_validation failed: result={res.json()}"
        await asyncio.sleep(1)

    @pytest.mark.parametrize(
        "test_data", generate_wildcard_test_case_for_validation(), ids=lambda d: d["model_schema_id"]
    )
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_016-017")
    async def test_wildcard_validation(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        provider_model_id = test_data["provider_model_id"]
        model_type = test_data["model_type"]
        credentials = {
            key: provider_credentials.aes_decrypt(test_data["credentials"][key])
            for key in test_data["credentials"].keys()
        }

        request_data = {
            "model_schema_id": model_schema_id,
            "provider_model_id": provider_model_id,
            "model_type": model_type,
            "credentials": credentials,
        }
        if model_type == "text_embedding":
            properties = test_data.get("properties", {})
            request_data = {**request_data, "properties": properties}

        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 200, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "success", f"test_validation failed: result={res.json()}"
        await asyncio.sleep(1.5)

    @pytest.mark.parametrize("test_data", generate_test_cases_for_validation(), ids=lambda d: d["model_schema_id"])
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_018")
    async def test_validation_with_error_credential(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        if "debug" in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        model_type = test_data["model_type"]
        if "custom_host" in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        credentials = {key: "12345678" for key in test_data["credentials"].keys()}
        request_data = {"model_schema_id": model_schema_id, "model_type": model_type, "credentials": credentials}
        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 400, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "PROVIDER_ERROR"
        await asyncio.sleep(1)

    @pytest.mark.parametrize("test_data", generate_test_cases_for_validation(), ids=lambda d: d["model_schema_id"])
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_018")
    async def test_custom_host_validation_with_error_credential(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        if "debug" in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        model_type = test_data["model_type"]
        if "custom_host" not in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")

        request_data = {
            "model_schema_id": "custom_host/openai-text-embedding",
            "model_type": "text_embedding",
            "credentials": {
                "CUSTOM_HOST_ENDPOINT_URL": "12345678",
                "CUSTOM_HOST_MODEL_ID": "text-embedding-3-small",
                "CUSTOM_HOST_API_KEY": Config.CUSTOM_HOST_API_KEY,
            },
            "properties": {"embedding_size": 1536},
        }

        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 422, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"

        request_data.update(
            {
                "model_schema_id": "custom_host/openai-text-embedding",
                "model_type": "text_embedding",
                "credentials": {
                    "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/embeddings",
                    "CUSTOM_HOST_MODEL_ID": "text-embedding-3-small",
                    "CUSTOM_HOST_API_KEY": "12345678",
                },
                "properties": {"embedding_size": 1536},
            }
        )

        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 400, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "PROVIDER_ERROR"
        await asyncio.sleep(1)

    @pytest.mark.parametrize(
        "test_data", generate_wildcard_test_case_for_validation(), ids=lambda d: d["model_schema_id"]
    )
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_018")
    async def test_wildcard_validation_with_error_credential(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        provider_model_id = test_data["provider_model_id"]
        model_type = test_data["model_type"]
        if "debug" in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        credentials = {key: "12345678" for key in test_data["credentials"].keys()}

        request_data = {
            "model_schema_id": model_schema_id,
            "provider_model_id": provider_model_id,
            "model_type": model_type,
            "credentials": credentials,
        }
        if model_type == "text_embedding":
            properties = test_data.get("properties", {})
            request_data = {**request_data, "properties": properties}

        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 400, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "PROVIDER_ERROR"

        await asyncio.sleep(1)

    @pytest.mark.parametrize(
        "test_data", generate_wildcard_test_case_for_validation(), ids=lambda d: d["model_schema_id"]
    )
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_019")
    async def test_wildcard_validation_with_no_properties(self, test_data):
        model_schema_id = test_data["model_schema_id"]
        provider_model_id = test_data["provider_model_id"]
        model_type = test_data["model_type"]
        credentials = {
            key: provider_credentials.aes_decrypt(test_data["credentials"][key])
            for key in test_data["credentials"].keys()
        }

        request_data = {
            "model_schema_id": model_schema_id,
            "provider_model_id": provider_model_id,
            "model_type": model_type,
            "credentials": credentials,
        }
        if model_type == "text_embedding":
            try:
                res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
            except asyncio.TimeoutError:
                pytest.skip("Skipping test due to timeout after 2 minutes.")
            assert res.status_code == 422, f"test_validation failed: result={res.json()}"
            assert res.json()["status"] == "error"
            assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"
        else:
            pytest.skip("Test not applicable for this model type")
        await asyncio.sleep(1)

    @pytest.mark.parametrize("test_data", generate_test_cases_for_validation(), ids=lambda d: d["model_schema_id"])
    @pytest.mark.parametrize("provider_url", Config.PROVIDER_URL_BLACK_LIST)
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_028")
    async def test_validation_with_error_provider_url(self, test_data, provider_url):
        model_schema_id = test_data["model_schema_id"]
        print("model_schema_id: ", model_schema_id)
        if "custom_host" not in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        model_type = test_data["model_type"]
        credentials = {
            key: provider_credentials.aes_decrypt(test_data["credentials"][key])
            for key in test_data["credentials"].keys()
        }
        for key in credentials.keys():
            if "URL" in key:
                credentials[key] = provider_url
                break
        request_data = {"model_schema_id": model_schema_id, "model_type": model_type, "credentials": credentials}
        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 422, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"
        await asyncio.sleep(1)

    @pytest.mark.parametrize("test_data", generate_test_cases_for_validation(), ids=lambda d: d["model_schema_id"])
    @pytest.mark.parametrize("provider_url", Config.PROVIDER_URL_BLACK_LIST)
    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_028")
    async def test_validation_with_error_proxy(self, test_data, provider_url):
        model_schema_id = test_data["model_schema_id"]
        if "openai" not in test_data["model_schema_id"]:
            pytest.skip("Test not applicable for this model type")
        model_type = test_data["model_type"]
        credentials = {
            key: provider_credentials.aes_decrypt(test_data["credentials"][key])
            for key in test_data["credentials"].keys()
        }
        custom_headers = {"Helicone-Auth": f"Bearer {Config.HELICONE_API_KEY}"}
        request_data = {
            "model_schema_id": model_schema_id,
            "model_type": model_type,
            "credentials": credentials,
            "proxy": provider_url,
            "custom_headers": custom_headers,
        }
        try:
            res = await asyncio.wait_for(verify_credentials(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        assert res.status_code == 422, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"
        await asyncio.sleep(1)

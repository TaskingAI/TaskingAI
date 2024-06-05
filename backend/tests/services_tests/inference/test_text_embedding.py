import pytest

from backend.tests.api_services.inference.text_embedding import text_embedding
from backend.tests.common.config import CONFIG


@pytest.mark.api_test
class TestTextEmbedding:

    input_list = [{"input": "hello, nice to meet you"}, {"input": ["hello, nice to meet you", "i'm fine thank you"]}]

    long_list_text = {"input": ["*" * 600, "!" * 600]}
    empty_list_text = {"input": []}

    error_input_list = [
        {"input": 100},
        {"input": ["hello, nice to meet you", 100]},
    ]

    @pytest.mark.run(order=121)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", input_list)
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_001-002")
    async def test_text_embedding(self, input_data):

        text_embedding_model_id_list = [
            CONFIG.text_embedding_model_id,
            CONFIG.togetherai_text_embedding_model_id,
            CONFIG.custom_host_text_embedding_model_id,
            CONFIG.fallbacks_text_embedding_model_id,
        ]

        for model_id in text_embedding_model_id_list:
            input_data.update({"model_id": model_id})
            res = await text_embedding(input_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            for item in res_json.get("data"):
                assert all(isinstance(value, float) for value in item.get("embedding"))

    @pytest.mark.run(order=122)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_004")
    async def test_text_embedding_with_long_list_text(self):

        text_embedding_model_id_list = [
            CONFIG.text_embedding_model_id,
            CONFIG.togetherai_text_embedding_model_id,
            CONFIG.custom_host_text_embedding_model_id,
            CONFIG.fallbacks_text_embedding_model_id,
        ]

        for model_id in text_embedding_model_id_list:
            self.long_list_text.update({"model_id": model_id})
            res = await text_embedding(self.long_list_text)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            for item in res_json.get("data"):
                assert all(isinstance(value, float) for value in item.get("embedding"))


    @pytest.mark.run(order=123)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_004")
    async def test_text_embedding_with_empty_list_text(self):

        text_embedding_model_id_list = [
            CONFIG.text_embedding_model_id,
            CONFIG.togetherai_text_embedding_model_id,
            CONFIG.custom_host_text_embedding_model_id,
            CONFIG.fallbacks_text_embedding_model_id,

        ]

        for model_id in text_embedding_model_id_list:
            self.empty_list_text.update({"model_id": model_id})
            res = await text_embedding(self.empty_list_text)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            for item in res_json.get("data"):
                assert all(isinstance(value, float) for value in item.get("embedding"))

    @pytest.mark.run(order=124)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", error_input_list)
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("inference_003")
    async def test_error_text_embedding(self, input_data):

        text_embedding_model_id_list = [
            CONFIG.text_embedding_model_id,
            CONFIG.togetherai_text_embedding_model_id,
            CONFIG.custom_host_text_embedding_model_id,
            CONFIG.fallbacks_text_embedding_model_id,

        ]

        for model_id in text_embedding_model_id_list:
            input_data.update({"model_id": model_id})
            res = await text_embedding(input_data)
            res_json = res.json()

            assert res.status_code == 422, res.json()
            assert res_json.get("status") == "error"
            assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

import allure
import pytest
import asyncio
from test.inference_service.inference import rerank
from .utils.utils import generate_test_cases, generate_wildcard_test_cases, check_order, is_provider_service_error
from test.setting import Config


@allure.epic("inference_service")
@allure.feature("rerank")
class TestRerank:
    query = "Organic skincare products for sensitive skin"
    documents = [
        "Eco-friendly kitchenware for modern homes",
        "Biodegradable cleaning supplies for eco-conscious consumers",
        "Organic cotton baby clothes for sensitive skin",
        "Natural organic skincare range for sensitive skin",
        "Tech gadgets for smart homes: 2024 edition",
        "Sustainable gardening tools and compost solutions",
        "Sensitive skin-friendly facial cleansers and toners",
        "Organic food wraps and storage solutions",
        "All-natural pet food for dogs with allergies",
        "Yoga mats made from recycled materials",
    ]
    top_n = 3

    error_input_list = [
        {"model_schema_id": 100},
        {"query": 100},
        {"documents": 100},
        {"top_n": "3"},
        {"model_schema_id": ""},
        {"query": ""},
        {"documents": []},
        {"top_n": 0},
        {
            "model_schema_id": "0123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899"
        },
        {"documents": [100]},
        {"documents": [""]},
    ]

    less_input_list = [
        {"query": query, "documents": documents, "top_n": top_n},
        {"model_schema_id": "jina-colbert-v1-en", "documents": documents, "top_n": top_n},
        {"model_schema_id": "jina-colbert-v1-en", "query": query, "top_n": top_n},
        {"model_schema_id": "jina-colbert-v1-en", "query": query, "documents": documents},
    ]

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_031")
    @pytest.mark.parametrize(
        "test_data",
        generate_test_cases("rerank") + generate_wildcard_test_cases("rerank"),
        ids=lambda d: d["model_schema_id"],
    )
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    async def test_rerank(self, test_data):
        model_schema_id = test_data["model_schema_id"]

        request_data = {
            "model_schema_id": model_schema_id,
            "query": self.query,
            "documents": self.documents,
            "top_n": self.top_n,
        }
        try:
            res = await asyncio.wait_for(rerank(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        results = res_json.get("data").get("results")
        assert len(results) == self.top_n
        assert check_order(results, "relevance_score")
        for result in results:
            assert result.get("document").get("text") in self.documents
            assert result.get("relevance_score") >= 0.0
            if "jina-colbert-v1-en" in model_schema_id:
                assert result.get("relevance_score") <= 10.0
            else:
                assert result.get("relevance_score") <= 1.0
            assert result.get("index") == self.documents.index(result.get("document").get("text"))

    @pytest.mark.test_id("inference_032")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", error_input_list)
    @pytest.mark.parametrize("test_data", generate_test_cases("rerank"), ids=lambda d: d["model_schema_id"])
    async def test_error_rerank(self, input_data, test_data):
        request_data = {}
        if input_data.get("model_schema_id") is None:
            request_data.update({"model_schema_id": test_data["model_schema_id"]})
        if input_data.get("query") is None:
            request_data.update({"query": self.query})
        if input_data.get("documents") is None:
            request_data.update({"documents": self.documents})
        if input_data.get("top_n") is None:
            request_data.update({"top_n": self.top_n})
        try:
            res = await asyncio.wait_for(rerank(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        res_json = res.json()
        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_033")
    @pytest.mark.parametrize("test_data", less_input_list)
    async def test_less_rerank(self, test_data):
        res = await rerank(test_data)
        res_json = res.json()
        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_031")
    @pytest.mark.parametrize("provider_url", Config.PROVIDER_URL_BLACK_LIST)
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    async def test_rerank_with_error_proxy(self, provider_url):
        model_schema_id = "cohere/rerank-english-v2.0"
        request_data = {
            "model_schema_id": model_schema_id,
            "query": self.query,
            "documents": self.documents,
            "top_n": self.top_n,
            "proxy": provider_url,
        }
        try:
            res = await asyncio.wait_for(rerank(request_data), timeout=120)
        except asyncio.TimeoutError:
            pytest.skip("Skipping test due to timeout after 2 minutes.")
        if is_provider_service_error(res):
            pytest.skip(f"Skip the test case with provider service error.")
        assert res.status_code == 422, f"test_validation failed: result={res.json()}"
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"

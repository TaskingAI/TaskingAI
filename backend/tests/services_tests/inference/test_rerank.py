import pytest

from backend.tests.api_services.inference.rerank import rerank
from backend.tests.common.config import CONFIG
from backend.tests.common.utils import check_order


@pytest.mark.api_test
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
        {"model_id": 100},
        {"query": 100},
        {"documents": 100},
        {"top_n": "3"},
        {"model_id": ""},
        {"query": ""},
        {"documents": []},
        {"top_n": 0},
        {
            "model_id": "0123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899"
        },
        {"documents": [100]},
        {"documents": [""]},
    ]

    less_input_list = [
        {"query": query, "documents": documents, "top_n": top_n},
        {"model_id": CONFIG.rerank_model_id, "documents": documents, "top_n": top_n},
        {"model_id": CONFIG.rerank_model_id, "query": query, "top_n": top_n},
        {"model_id": CONFIG.rerank_model_id, "query": query, "documents": documents},
    ]

    @pytest.mark.asyncio
    @pytest.mark.run(order=121)
    @pytest.mark.version("0.3.2")
    @pytest.mark.test_id("inference_051")
    async def test_rerank(self):
        rerank_model_list = [CONFIG.rerank_model_id, CONFIG.fallbacks_rerank_model_id]
        for model_id in rerank_model_list:
            request_data = {
                "model_id": model_id,
                "query": self.query,
                "documents": self.documents,
                "top_n": self.top_n,
            }
            res = await rerank(request_data)
            res_json = res.json()
            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            results = res_json.get("data").get("results")
            assert len(results) == self.top_n
            assert check_order(results, "relevance_score")
            for result in results:
                assert result.get("document").get("text") in self.documents
                assert result.get("relevance_score") >= 0.0
                assert result.get("relevance_score") <= 1.0
                assert result.get("index") == self.documents.index(result.get("document").get("text"))

    @pytest.mark.asyncio
    @pytest.mark.run(order=122)
    @pytest.mark.version("0.3.2")
    @pytest.mark.test_id("inference_052")
    @pytest.mark.parametrize("input_data", error_input_list)
    async def test_error_rerank(self, input_data):
        request_data = {}
        if input_data.get("model_id") is None:
            request_data.update({"model_id": CONFIG.rerank_model_id})
        if input_data.get("query") is None:
            request_data.update({"query": self.query})
        if input_data.get("documents") is None:
            request_data.update({"documents": self.documents})
        if input_data.get("top_n") is None:
            request_data.update({"top_n": self.top_n})
        res = await rerank(request_data)
        res_json = res.json()
        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.asyncio
    @pytest.mark.run(order=123)
    @pytest.mark.version("0.3.2")
    @pytest.mark.test_id("inference_053")
    @pytest.mark.parametrize("test_data", less_input_list)
    async def test_less_rerank(self, test_data):
        res = await rerank(test_data)
        res_json = res.json()
        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

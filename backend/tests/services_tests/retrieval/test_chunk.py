import pytest

from tests.services_api.retrieval.chunk import query_chunks
from tests.services_tests.retrieval import Retrieval


class TestChunk(Retrieval):

    chunk_list = ["object", "chunk_id", "record_id", "collection_id", "content", "metadata", "updated_timestamp",
                  "created_timestamp", "score"]
    chunk_keys = set(chunk_list)

    @pytest.mark.run(order=39)
    @pytest.mark.asyncio
    async def test_success_query_chunk(self):

        query_chunks_data = {
            "query_text": "test",
            "top_k": 1
        }
        query_chunks_res = await query_chunks(Retrieval.collection_id, query_chunks_data)
        query_chunks_res_json = query_chunks_res.json()
        assert query_chunks_res.status_code == 200
        assert query_chunks_res_json.get("status") == "success"
        assert query_chunks_res_json.get("fetched_count") == 1
        for chunk in query_chunks_res_json.get("data"):
            assert isinstance(chunk.get("score"), float)
            assert set(chunk.keys()) == self.chunk_keys

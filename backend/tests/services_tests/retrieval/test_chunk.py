import pytest

from tests.services_api.retrieval.chunk import (query_chunks, list_collection_chunks, list_record_chunks, create_chunk,
                                                get_chunk, update_chunk, delete_chunk)
from tests.services_tests.retrieval import Retrieval


class TestChunk(Retrieval):

    chunk_list = ["object", "chunk_id", "record_id", "collection_id", "content", "num_tokens", "metadata",
                  "updated_timestamp", "created_timestamp"]
    chunk_keys = set(chunk_list)

    @pytest.mark.run(order=39)
    @pytest.mark.asyncio
    async def test_query_chunk(self):

        query_chunks_data = {
            "query_text": "test",
            "top_k": 1
        }
        query_chunks_res = await query_chunks(Retrieval.collection_id, query_chunks_data)
        query_chunks_res_json = query_chunks_res.json()
        assert query_chunks_res.status_code == 200
        assert query_chunks_res_json.get("status") == "success"
        assert len(query_chunks_res_json.get("data")) == 1
        assert query_chunks_res_json.get("fetched_count") == 1
        assert query_chunks_res_json.get("total_count") is None
        assert query_chunks_res_json.get("has_more") is None
        for chunk in query_chunks_res_json.get("data"):
            assert isinstance(chunk.get("score"), float)
            chunk.pop("score")
            assert set(chunk.keys()) == self.chunk_keys

    @pytest.mark.run(order=40)
    @pytest.mark.asyncio
    async def test_create_chunk(self):

        create_chunk_data = {
            "content": "This is a test for create chunk.",
            "metadata": {
                "key1": "value1"
            }
        }
        res = await create_chunk(Retrieval.collection_id, create_chunk_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("record_id") is None
        assert res_json.get("data").get("num_tokens") > 0
        for key in create_chunk_data:
            assert res_json.get("data").get(key) == create_chunk_data[key]
        assert set(res_json.get("data").keys()) == self.chunk_keys
        Retrieval.chunk_id = res_json.get("data").get("chunk_id")

    @pytest.mark.run(order=41)
    @pytest.mark.asyncio
    async def test_get_chunk(self):

        chunk_res = await get_chunk(Retrieval.collection_id, Retrieval.chunk_id)
        chunk_res_json = chunk_res.json()
        assert chunk_res.status_code == 200
        assert chunk_res_json.get("status") == "success"
        assert chunk_res_json.get("data").get("chunk_id") == Retrieval.chunk_id
        assert chunk_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert chunk_res_json.get("data").get("record_id") is None
        assert chunk_res_json.get("data").get("num_tokens") > 0
        assert set(chunk_res_json.get("data").keys()) == self.chunk_keys

    @pytest.mark.run(order=42)
    @pytest.mark.asyncio
    async def test_update_chunk(self):

        update_chunk_data = {
            "content": "This is a test for update chunk.",
            "metadata": {
                "key1": "value1"
            }
        }
        res = await update_chunk(Retrieval.collection_id, Retrieval.chunk_id, update_chunk_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("chunk_id") == Retrieval.chunk_id
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("record_id") is None
        assert res_json.get("data").get("num_tokens") > 0
        for key in update_chunk_data:
            assert res_json.get("data").get(key) == update_chunk_data[key]
        assert set(res_json.get("data").keys()) == self.chunk_keys

    @pytest.mark.run(order=43)
    @pytest.mark.asyncio
    async def test_list_collection_chunks(self):

        list_collection_chunks_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": Retrieval.chunk_id[:8]
        }
        res = await list_collection_chunks(self.collection_id, list_collection_chunks_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        assert len(res_json.get("data")) == 1
        assert res_json.get("fetched_count") == 1
        assert res_json.get("total_count") == 1
        assert res_json.get("has_more") is False

    @pytest.mark.run(order=44)
    @pytest.mark.asyncio
    async def test_list_record_chunks(self):

        list_record_chunks_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": Retrieval.chunk_id[:4]
        }

        res = await list_record_chunks(self.collection_id, self.record_id, list_record_chunks_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == res_json.get("fetched_count") >= 1
        assert res_json.get("total_count") >= 1
        assert res_json.get("has_more") is False or True

    @pytest.mark.run(order=45)
    @pytest.mark.asyncio
    async def test_delete_chunk(self):

        res = await delete_chunk(self.collection_id, self.chunk_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"

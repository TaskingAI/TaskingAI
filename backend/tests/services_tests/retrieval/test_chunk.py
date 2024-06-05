import pytest
import json
from backend.tests.api_services.retrieval.chunk import (query_chunks, list_collection_chunks, list_record_chunks, create_chunk,
                                           get_chunk, update_chunk, delete_chunk)
from backend.tests.services_tests.retrieval import Retrieval
from backend.tests.common.config import CONFIG


@pytest.mark.api_test
class TestChunk(Retrieval):


    @pytest.mark.run(order=151)
    @pytest.mark.asyncio
    async def test_query_chunk(self):

        query_chunks_data_list = [
            {
                "query_text": "TaskingAI",
                "top_k": 1,
                "score_threshold": 0.01
            },
            {
                "query_text": "TaskingAI",
                "top_k": 1,
                "max_tokens": 20000
            },
            {
                "query_text": "TaskingAI",
                "top_k": 1,
                "rerank_model_id": CONFIG.rerank_model_id
            }
        ]

        for query_chunks_data in query_chunks_data_list:
            query_chunks_res = await query_chunks(Retrieval.collection_id, query_chunks_data)
            query_chunks_res_json = query_chunks_res.json()

            assert query_chunks_res.status_code == 200,  query_chunks_res.json()
            assert query_chunks_res_json.get("status") == "success"
            assert len(query_chunks_res_json.get("data")) == 1
            assert query_chunks_res_json.get("fetched_count") == 1

            if query_chunks_res_json.get("has_more") is not None:
                assert query_chunks_res_json.get("has_more") is False
            else:
                assert query_chunks_res_json.get("has_more") is None
            for chunk in query_chunks_res_json.get("data"):
                assert isinstance(chunk.get("score"), float)

            if query_chunks_data.get("max_tokens"):
                assert query_chunks_res_json.get("data")[0].get("num_tokens") <= query_chunks_data.get("max_tokens")
            if query_chunks_data.get("score_threshold"):
                assert query_chunks_res_json.get("data")[0].get("score") >= query_chunks_data.get("score_threshold")


    @pytest.mark.run(order=152)
    @pytest.mark.asyncio
    async def test_create_chunk(self):

        create_chunk_data_list = [
            {
                "content": "This is a test for create chunk.",
                "metadata": {
                    "key1": "value1"
                }
            },
            {
                "content": "Openai is a platform for creating and managing AI tasks.",
            }
        ]
        for create_chunk_data in create_chunk_data_list:
            res = await create_chunk(Retrieval.collection_id, create_chunk_data)
            res_json = res.json()

            assert res.status_code == 200,  res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert res_json.get("data").get("record_id") is None
            assert res_json.get("data").get("num_tokens") > 0
            for key in create_chunk_data:
                assert res_json.get("data").get(key) == create_chunk_data[key]

            Retrieval.chunk_id = res_json.get("data").get("chunk_id")

            get_res = await get_chunk(Retrieval.collection_id, Retrieval.chunk_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200,  get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert get_res_json.get("data").get("chunk_id") == Retrieval.chunk_id
            assert get_res_json.get("data").get("record_id") is None
            assert get_res_json.get("data").get("num_tokens") > 0
            for key in create_chunk_data:
                assert get_res_json.get("data").get(key) == create_chunk_data[key]


    @pytest.mark.run(order=153)
    @pytest.mark.asyncio
    async def test_get_chunk(self):
        chunk_res = await get_chunk(Retrieval.collection_id, Retrieval.chunk_id)
        chunk_res_json = chunk_res.json()

        assert chunk_res.status_code == 200,  chunk_res.json()
        assert chunk_res_json.get("status") == "success"
        assert chunk_res_json.get("data").get("chunk_id") == Retrieval.chunk_id
        assert chunk_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert chunk_res_json.get("data").get("record_id") is None
        assert chunk_res_json.get("data").get("num_tokens") > 0


    @pytest.mark.run(order=154)
    @pytest.mark.asyncio
    async def test_update_chunk(self):

        update_chunk_data_list = [
            {
                "content": "This is a test for update chunk.",
            },
            {
                "metadata": {
                    "key1": "value1"
                }
            }
        ]

        for update_chunk_data in update_chunk_data_list:

            res = await update_chunk(Retrieval.collection_id, Retrieval.chunk_id, update_chunk_data)
            res_json = res.json()

            assert res.status_code == 200,  res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("chunk_id") == Retrieval.chunk_id
            assert res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert res_json.get("data").get("record_id") is None
            assert res_json.get("data").get("num_tokens") > 0
            for key in update_chunk_data:
                assert res_json.get("data").get(key) == update_chunk_data[key]


            get_res = await get_chunk(Retrieval.collection_id, Retrieval.chunk_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200,  get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("chunk_id") == Retrieval.chunk_id
            assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert get_res_json.get("data").get("record_id") is None
            assert get_res_json.get("data").get("num_tokens") > 0
            for key in update_chunk_data:
                assert get_res_json.get("data").get(key) == update_chunk_data[key]

    @pytest.mark.run(order=155)
    @pytest.mark.asyncio
    async def test_list_collection_chunks(self):

        list_collection_chunks_data_list = [
            {
                "limit": 10,
                "order": "desc",
                "after": Retrieval.chunk_id
            },
            {
                "limit": 10,
                "order": "asc",
                "prefix_filter": json.dumps({"chunk_id": Retrieval.chunk_id[:12]}),
            }
        ]
        for list_collection_chunks_data in list_collection_chunks_data_list:
            if "API" in CONFIG.TEST_MODE:
                if list_collection_chunks_data.get("prefix_filter"):
                    continue
            res = await list_collection_chunks(self.collection_id, list_collection_chunks_data)
            res_json = res.json()

            assert res.status_code == 200,  res.json()
            assert res.json().get("status") == "success"
            if list_collection_chunks_data.get("prefix_filter"):
                assert len(res_json.get("data")) == res_json.get("fetched_count") == 1
                assert res_json.get("has_more") is False
                prefix_filter_dict = json.loads(list_collection_chunks_data.get("prefix_filter"))
                for key in prefix_filter_dict:
                    assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))
            else:
                assert len(res_json.get("data")) == res_json.get("fetched_count") >= 1
                assert res_json.get("has_more") is True

    @pytest.mark.run(order=156)
    @pytest.mark.asyncio
    async def test_list_record_chunks(self):
        if "TASKINGAI_WEB" in CONFIG.TEST_MODE:

            list_record_chunks_data = {
                "limit": 10,
                "order": "desc",
                "id_search": Retrieval.chunk_id[:4]
            }

            res = await list_record_chunks(self.collection_id, self.record_id, list_record_chunks_data)
            res_json = res.json()
            assert res.status_code == 200,  res.json()
            assert res_json.get("status") == "success"
            assert len(res_json.get("data")) == res_json.get("fetched_count") >= 1
            assert res_json.get("has_more") is False or True

    @pytest.mark.run(order=157)
    @pytest.mark.asyncio
    async def test_delete_chunk(self):

        res = await delete_chunk(self.collection_id, Retrieval.chunk_id)
        res_json = res.json()
        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"

        get_res = await get_chunk(self.collection_id, Retrieval.chunk_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 404, get_res.json()
        assert get_res_json.get("status") == "error"
        assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"


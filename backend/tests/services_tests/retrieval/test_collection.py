import pytest

from tests.services_api.retrieval.collection import (create_collection, get_collection, list_collections,
                                                     update_collection, delete_collection)
from tests.services_api.model.model import create_model
from tests.services_tests.retrieval import Retrieval


class TestCollection(Retrieval):

    data_list = ['object', 'collection_id', 'name', 'description', 'num_records', 'num_chunks', 'capacity',
                 'embedding_model_id', 'embedding_size', 'metadata',  'updated_timestamp', 'created_timestamp',
                 'status',  "text_splitter"]
    data_keys = set(data_list)
    data_text_splitter = ["type", "chunk_size", "chunk_overlap"]
    data_text_splitter_keys = set(data_text_splitter)

    @pytest.mark.run(order=31)
    @pytest.mark.asyncio
    async def test_create_collection(self):

        create_text_embedding_model_data = {
            "name": "My Embedding Model",
            "model_schema_id": "openai/text-embedding-ada-002",
            "credentials": {"OPENAI_API_KEY": "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"}
        }

        create_text_embedding_model_res = await create_model(create_text_embedding_model_data)
        create_text_embedding_model_res_json = create_text_embedding_model_res.json()
        text_embedding_model_id = create_text_embedding_model_res_json.get("data").get("model_id")

        create_collection_data = {
                                    "capacity": 1000,
                                    "embedding_model_id": text_embedding_model_id,
                                    "name": "test",
                                    "description": "description",
                                    "text_splitter": {
                                        "type": "token",
                                        "chunk_size": 200,
                                        "chunk_overlap": 100
                                    },
                                    "metadata": {
                                        "key1": "value1",
                                        "key2": "value2"
                                    }
                                }
        res = await create_collection(create_collection_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("status") == "ready"
        assert set(res_json.get("data").keys()) == self.data_keys
        assert set(res_json.get("data").get("text_splitter").keys()) == self.data_text_splitter_keys
        for key in create_collection_data:
            assert res_json.get("data").get(key) == create_collection_data[key]
        Retrieval.collection_id = res_json.get("data").get("collection_id")
        Retrieval.collection_name = res_json.get("data").get("name")

    @pytest.mark.run(order=32)
    @pytest.mark.asyncio
    async def test_get_collection(self):

        collection_res = await get_collection(self.collection_id)
        collection_json = collection_res.json()
        assert collection_res.status_code == 200
        assert collection_json.get("status") == "success"
        assert collection_json.get("data").get("status") == "ready"
        assert set(collection_json.get("data").keys()) == self.data_keys
        assert set(collection_json.get("data").get("text_splitter").keys()) == self.data_text_splitter_keys

    @pytest.mark.run(order=33)
    @pytest.mark.asyncio
    async def test_list_collections(self):

        list_collections_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": Retrieval.collection_id[:4],
            "name_search": Retrieval.collection_name[:2],
        }
        res = await list_collections(list_collections_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("fetched_count") == 1
        assert res_json.get("total_count") == 1
        assert res_json.get("has_more") is False

    @pytest.mark.run(order=34)
    @pytest.mark.asyncio
    async def test_update_collection(self):
        update_collection_data = {
            "name": "test_update",
            "description": "description_update",
            "metadata": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        res = await update_collection(Retrieval.collection_id, update_collection_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("status") == "ready"
        assert set(res_json.get("data").keys()) == self.data_keys
        assert set(res_json.get("data").get("text_splitter").keys()) == self.data_text_splitter_keys
        for key in update_collection_data:
            assert res_json.get("data").get(key) == update_collection_data[key]

    @pytest.mark.run(order=41)
    @pytest.mark.asyncio
    async def test_delete_collection(self):

        res = await delete_collection(Retrieval.collection_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"

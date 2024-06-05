import pytest
import json
import asyncio
from backend.tests.api_services.retrieval.collection import (
    create_collection,
    get_collection,
    list_collections,
    update_collection,
    delete_collection,
    list_ui_collections,
    get_ui_collection,
)
from backend.tests.api_services.retrieval.record import create_record, get_record, update_record
from backend.tests.api_services.retrieval.chunk import create_chunk
from backend.tests.services_tests.retrieval import Retrieval
from backend.tests.common.config import CONFIG


@pytest.mark.api_test
class TestCollection(Retrieval):

    @pytest.mark.run(order=131)
    @pytest.mark.asyncio
    async def test_create_collection(self):

        create_collection_data_list = [
            {
                "capacity": 1000,
                "embedding_model_id": CONFIG.text_embedding_model_id,
                "name": "test",
                "description": "description",
                "metadata": {"key1": "value1", "key2": "value2"},
            },
            {
                "capacity": 1000,
                "embedding_model_id": CONFIG.text_embedding_model_id,
            },
        ]

        for create_collection_data in create_collection_data_list:

            res = await create_collection(create_collection_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("status") == "ready"

            for key in create_collection_data:
                assert res_json.get("data").get(key) == create_collection_data[key]
            Retrieval.collection_id = res_json.get("data").get("collection_id")
            if create_collection_data.get("name"):
                Retrieval.collection_name = res_json.get("data").get("name")
            get_res = await get_collection(Retrieval.collection_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200, get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("status") == "ready"
            assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id

            for key in create_collection_data:
                assert get_res_json.get("data").get(key) == create_collection_data[key]

    @pytest.mark.run(order=131)
    @pytest.mark.asyncio
    async def test_create_collection_with_not_support_capacity(self):

        create_collection_data = {
            "capacity": 900,
            "embedding_model_id": CONFIG.text_embedding_model_id,
        }

        res = await create_collection(create_collection_data)
        res_json = res.json()

        assert res.status_code == 422
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"

    @pytest.mark.run(order=132)
    @pytest.mark.asyncio
    async def test_get_collection(self):

        collection_res = await get_collection(self.collection_id)
        collection_json = collection_res.json()

        assert collection_res.status_code == 200, collection_res.json()
        assert collection_json.get("status") == "success"
        assert collection_json.get("data").get("status") == "ready"
        assert collection_json.get("data").get("collection_id") == self.collection_id

    @pytest.mark.run(order=132)
    @pytest.mark.asyncio
    async def test_get_ui_collection(self):

        if "WEB" in CONFIG.TEST_MODE:

            collection_res = await get_ui_collection(self.collection_id)
            collection_json = collection_res.json()

            assert collection_res.status_code == 200, collection_res.json()
            assert collection_json.get("status") == "success"
            assert collection_json.get("data").get("status") == "ready"
            assert collection_json.get("data").get("collection_id") == self.collection_id
            assert collection_json.get("data").get("model_name") == "Openai Text Embedding Model"

    @pytest.mark.run(order=133)
    @pytest.mark.asyncio
    async def test_list_collections(self):

        list_collections_data_list = [
            {
                "limit": 10,
                "order": "desc",
                "after": Retrieval.collection_id,
            },
            {
                "limit": 10,
                "order": "asc",
                "prefix_filter": json.dumps({"name": Retrieval.collection_name[:4]}),
            },
            {
                "limit": 10,
                "order": "desc",
                "prefix_filter": json.dumps({"collection_id": Retrieval.collection_id[:14]}),
            },
        ]
        for list_collections_data in list_collections_data_list:
            if "API" in CONFIG.TEST_MODE:
                if list_collections_data.get("prefix_filter"):
                    continue
            res = await list_collections(list_collections_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert len(res_json.get("data")) == 1
            assert res_json.get("fetched_count") == 1
            assert res_json.get("has_more") is False
            if list_collections_data.get("prefix_filter"):
                prefix_filter_dict = json.loads(list_collections_data.get("prefix_filter"))
                for key in prefix_filter_dict:
                    assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))

    @pytest.mark.run(order=133)
    @pytest.mark.asyncio
    async def test_list_ui_collections(self):

        if "WEB" in CONFIG.TEST_MODE:
            list_ui_collections_data_list = [
                {
                    "limit": 10,
                    "order": "desc",
                    "after": Retrieval.collection_id,
                },
                {
                    "limit": 10,
                    "order": "asc",
                    "prefix_filter": json.dumps({"name": Retrieval.collection_name[:4]}),
                },
                {
                    "limit": 10,
                    "order": "desc",
                    "prefix_filter": json.dumps({"collection_id": Retrieval.collection_id[:14]}),
                },
            ]
            for list_ui_collections_data in list_ui_collections_data_list:

                res = await list_ui_collections(list_ui_collections_data)
                res_json = res.json()

                assert res.status_code == 200, res.json()
                assert res_json.get("status") == "success"
                assert len(res_json.get("data")) == 1
                assert res_json.get("fetched_count") == 1
                assert res_json.get("has_more") is False
                if list_ui_collections_data.get("prefix_filter"):
                    prefix_filter_dict = json.loads(list_ui_collections_data.get("prefix_filter"))
                    for key in prefix_filter_dict:
                        assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))
                assert res_json.get("data")[0].get("model_name") == "Openai Text Embedding Model"

    @pytest.mark.run(order=134)
    @pytest.mark.asyncio
    async def test_update_collection(self):

        update_collection_data_list = [
            {
                "name": "test_update",
            },
            {
                "description": "description_update",
            },
            {"metadata": {"key1": "value1", "key2": "value2"}},
        ]
        for update_collection_data in update_collection_data_list:
            res = await update_collection(Retrieval.collection_id, update_collection_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("status") == "ready"
            assert res_json.get("data").get("collection_id") == Retrieval.collection_id

            for key in update_collection_data:
                assert res_json.get("data").get(key) == update_collection_data[key]

            get_res = await get_collection(Retrieval.collection_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200, get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("status") == "ready"
            assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id

            for key in update_collection_data:
                assert get_res_json.get("data").get(key) == update_collection_data[key]


    @pytest.mark.run(order=230)
    @pytest.mark.asyncio
    async def test_delete_collection(self):

        collections = await list_collections({"limit": 100})
        collection_ids = [collection.get("collection_id") for collection in collections.json().get("data")]
        for collection_id in collection_ids:

            res = await delete_collection(collection_id)
            res_json = res.json()
            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"

            get_res = await get_collection(collection_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 404, get_res.json()
            assert get_res_json.get("status") == "error"
            assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"

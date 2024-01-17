import pytest

from tests.services_api.retrieval.record import create_record, get_record, list_records, update_record, delete_record
from tests.services_tests.retrieval import Retrieval


class TestRecord(Retrieval):

    data_list = ["object", 'record_id', 'collection_id',  'num_chunks', 'content',  'metadata', 'type',
                 'updated_timestamp', 'created_timestamp', 'status', "title"]
    data_keys = set(data_list)

    @pytest.mark.run(order=35)
    @pytest.mark.asyncio
    async def test_create_record(self):

        create_record_data = {
            "type": "text",
            "title": "test create record",
            "content": "This is a test for create record.",
            "metadata": {
                "key1": "value1"
            }
        }
        res = await create_record(Retrieval.collection_id, create_record_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        for key in create_record_data:
            assert res_json.get("data").get(key) == create_record_data[key]
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"
        assert set(res_json.get("data").keys()) == self.data_keys
        Retrieval.record_id = res_json.get("data").get("record_id")

    @pytest.mark.run(order=36)
    @pytest.mark.asyncio
    async def test_get_record(self):

        record_res = await get_record(Retrieval.collection_id, Retrieval.record_id)
        record_res_json = record_res.json()
        assert record_res.status_code == 200
        assert record_res_json.get("status") == "success"
        assert record_res_json.get("data").get("record_id") == Retrieval.record_id
        assert record_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert record_res_json.get("data").get("status") == "ready"
        assert set(record_res_json.get("data").keys()) == self.data_keys

    @pytest.mark.run(order=37)
    @pytest.mark.asyncio
    async def test_list_records(self):
        list_records_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": Retrieval.record_id[:5]
        }
        list_records_res = await list_records(Retrieval.collection_id, list_records_data)
        list_records_res_json = list_records_res.json()
        assert list_records_res.status_code == 200
        assert list_records_res_json.get("status") == "success"
        assert list_records_res_json.get("fetched_count") == 1
        assert list_records_res_json.get("total_count") == 1
        assert list_records_res_json.get("has_more") is False

    @pytest.mark.run(order=38)
    @pytest.mark.asyncio
    async def test_update_record(self):
        update_record_data = {
            "metadata": {
                "key2": "value2"
            }
        }
        res = await update_record(Retrieval.collection_id, Retrieval.record_id, update_record_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("record_id") == Retrieval.record_id
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"
        assert set(res_json.get("data").keys()) == self.data_keys
        for key in update_record_data:
            assert res_json.get("data").get(key) == update_record_data[key]

    @pytest.mark.run(order=40)
    @pytest.mark.asyncio
    async def test_delete_record(self):

        res = await delete_record(Retrieval.collection_id, Retrieval.record_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"

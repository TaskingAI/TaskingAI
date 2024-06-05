import pytest
import json
import os
import asyncio
from backend.tests.api_services.retrieval.collection import create_collection, get_collection
from backend.tests.api_services.retrieval.record import create_record, get_record, list_records, update_record, delete_record
from backend.tests.api_services.retrieval.chunk import list_record_chunks, delete_chunk
from backend.tests.services_tests.retrieval import Retrieval
from backend.tests.api_services.file.file import upload_file
from backend.tests.common.config import CONFIG


@pytest.mark.api_test
class TestRecord(Retrieval):

    record_list = ["object", 'record_id', 'collection_id',  'num_chunks', 'content',  'metadata', 'type',
                   'updated_timestamp', 'created_timestamp', 'status', "title"]
    record_keys = set(record_list)
    upload_file_list = []
    none_file_list = []
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    filenames = os.listdir(base_path + "/file")
    for filename in filenames:
        filepath = os.path.join(base_path, "file", filename)
        if os.path.isfile(filepath):
            upload_file_dict = {
                "module": "retrieval",
                "purpose": "record_file",
            }
            upload_file_dict.update({"file": filepath})
            upload_file_dict["file_name"] = filename
            if "test" in filename:
                upload_file_list.append(upload_file_dict)
            elif "none" in filename:
                none_file_list.append(upload_file_dict)

    @pytest.mark.run(order=141)
    @pytest.mark.asyncio
    async def test_create_record(self):

        create_record_data_list = [
            {
                "type": "text",
                "title": "TaskingAI Introduction",
                "content":
                    """Introduction
                       TaskingAI is an AI-native application development platform that unifies modules like Model, Retrieval, Assistant, and Tool into one seamless ecosystem, streamlining the creation and deployment of applications for developers.

                        Key Concepts
                        Project
                        Projects in TaskingAI are organizational units designed to group related activities and resources. They offer a structured way to manage different initiatives or brands, allowing for clear segregation and management. Each project can be tailored with specific config and resources, ensuring that the information and activities within one project remain distinct and isolated from others.

                        Model
                        TaskingAI incorporates a variety of chat completion models, each with distinct capabilities and attributes. These models serve as the core 'brains' of AI assistants, providing them with reasoning and logical capabilities. TaskingAI supports models from multiple providers, each offering different strengths in terms of input token limits, reasoning, and logic capabilities. Users can select and switch between models based on their specific needs and the complexity of the tasks at hand.

                        Retrieval
                        Retrievals in TaskingAI are mechanisms that enable AI assistants to access and utilize external knowledge bases. This feature allows the integration of additional information into the AI's responses, enhancing its ability to provide accurate and context-relevant answers. Retrievals are crucial for tasks that require specific, detailed, or up-to-date information, ensuring that the AI's responses are not limited by its pre-training data.

                        Assistant
                        The Assistant feature in TaskingAI refers to the AI entities capable of performing a wide range of tasks. These assistants are customizable and can be tailored to suit various applications, from customer service to internal training. They operate based on the models and tools provided, and their functionality can be extended through the use of retrievals, allowing them to access a broader range of information and capabilities.

                        Tool
                        Tools in TaskingAI are functionalities that enable AI assistants to interact with external resources and perform specific actions, such as fetching live information or communicating with external systems. These tools are typically defined in OpenAPI schema format and can be attached to assistants to enhance their capabilities. Tools are essential for tasks that require real-time data or interaction with external APIs and services, making the assistants more dynamic and versatile in their operation.

                        TaskingAI is more than just a platform; it's a gateway to unlocking the full potential of AI in your daily tasks. Whether you're a developer, a researcher, or someone looking to streamline their workflow, TaskingAI offers the tools and resources to achieve your goals.""",
                "text_splitter": {
                    "type": "token",
                    "chunk_size": 200,
                    "chunk_overlap": 100
                },
                "metadata": {
                    "key1": "value1"
                }
            },
            {"text_splitter": {
                    "type": "separator",
                    "separators": [",", "."],
                    "chunk_size": 200,
                    "chunk_overlap": 100
                },
                "content": "Egypt (Arabic: مصر Miṣr [mesˁr], Egyptian Arabic pronunciation: [mɑsˤr]), officially the Arab Republic of Egypt, is a transcontinental country spanning the northeast corner of Africa and the Sinai Peninsula in the southwest corner of Asia. It is bordered by the Mediterranean Sea to the north, the Gaza Strip of Palestine and Israel to the northeast, the Red Sea to the east, Sudan to the south, and Libya to the west."
            }
        ]

        for create_record_data in create_record_data_list:

            res = await create_record(Retrieval.collection_id, create_record_data)
            res_json = res.json()

            assert res.status_code == 200,  res.json()
            assert res_json.get("status") == "success"
            for key in create_record_data:
                if key == "text_splitter":
                    continue
                else:
                    assert res_json.get("data").get(key) == create_record_data[key]
            assert res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert res_json.get("data").get("status") == "ready"

            Retrieval.record_id = res_json.get("data").get("record_id")

            get_res = await get_record(Retrieval.collection_id, Retrieval.record_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200,  get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("record_id") == Retrieval.record_id
            assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert get_res_json.get("data").get("status") == "ready"

            for key in create_record_data:
                if key == "text_splitter":
                    continue
                else:
                    assert get_res_json.get("data").get(key) == create_record_data[key]

    @pytest.mark.run(order=141)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("upload_file_data", upload_file_list)
    async def test_create_record_with_file(self, upload_file_data):

        res = await upload_file(upload_file_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        file_id = res.json()["data"]["file_id"]
        assert file_id is not None

        create_record_data = {
            "type": "file",
            "file_id": file_id,
            "text_splitter": {"type": "token", "chunk_size": 200, "chunk_overlap": 100}
        }

        res = await create_record(Retrieval.collection_id, create_record_data)
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for key in create_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "file_id":
                content = json.loads(res_json.get("data").get("content"))
                assert content.get("file_id") == file_id
                assert content.get("file_name") == upload_file_data["file_name"]
                assert content.get("file_size") > 0
            else:
                assert res_json.get("data").get(key) == create_record_data[key]
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"

        record_id = res_json.get("data").get("record_id")

        get_res = await get_record(Retrieval.collection_id, record_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("record_id") == record_id
        assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert get_res_json.get("data").get("status") == "ready"

        for key in create_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "file_id":
                content = json.loads(res_json.get("data").get("content"))
                assert content.get("file_id") == file_id
                assert content.get("file_name") == upload_file_data["file_name"]
                assert content.get("file_size") > 0
            else:
                assert get_res_json.get("data").get(key) == create_record_data[key]
        # test file is exist
        await asyncio.sleep(1)
        res = await create_record(Retrieval.collection_id, create_record_data)
        res_json = res.json()
        assert res.status_code == 404, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "OBJECT_NOT_FOUND"


    @pytest.mark.run(order=141)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("upload_file_data", none_file_list)
    async def test_create_record_with_none_file(self, upload_file_data):

        res = await upload_file(upload_file_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        file_id = res.json()["data"]["file_id"]
        assert file_id is not None

        create_record_data = {
            "type": "file",
            "file_id": file_id,
            "text_splitter": {"type": "token", "chunk_size": 200, "chunk_overlap": 100}
        }

        res = await create_record(Retrieval.collection_id, create_record_data)
        res_json = res.json()
        assert res_json.get("status") == "error"

    @pytest.mark.run(order=141)
    @pytest.mark.asyncio
    async def test_create_record_with_web(self):

        create_record_data = {
            "type": "web",

            "url": "https://doc.adaprox.io/user-manuals/adfb0301-en",
            "text_splitter": {
                "type": "token",
                "chunk_size": 150,
                "chunk_overlap": 20
            }
        }

        res = await create_record(Retrieval.collection_id, create_record_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for key in create_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "url":
                assert create_record_data["url"] in res_json.get("data").get("content")
            else:
                assert res_json.get("data").get(key) == create_record_data[key]
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"

        record_id = res_json.get("data").get("record_id")

        get_res = await get_record(Retrieval.collection_id, record_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("record_id") == record_id
        assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert get_res_json.get("data").get("status") == "ready"

        for key in create_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "url":
                assert create_record_data["url"] in get_res_json.get("data").get("content")
            else:
                assert get_res_json.get("data").get(key) == create_record_data[key]

    @pytest.mark.run(order=142)
    @pytest.mark.asyncio
    async def test_get_record(self):

        record_res = await get_record(Retrieval.collection_id, Retrieval.record_id)
        record_res_json = record_res.json()

        assert record_res.status_code == 200,  record_res.json()
        assert record_res_json.get("status") == "success"
        assert record_res_json.get("data").get("record_id") == Retrieval.record_id
        assert record_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert record_res_json.get("data").get("status") == "ready"


    @pytest.mark.run(order=143)
    @pytest.mark.asyncio
    async def test_list_records(self):

        list_records_data_list = [
            {
                "limit": 10,
                "order": "desc",
                "after": Retrieval.record_id,
            },
            {
                "limit": 10,
                "order": "asc",
                "prefix_filter": json.dumps({"record_id": Retrieval.record_id[:8]}),
            }
        ]

        for list_records_data in list_records_data_list:
            if "API" in CONFIG.TEST_MODE:
                if list_records_data.get("prefix_filter"):
                    continue
            list_records_res = await list_records(Retrieval.collection_id, list_records_data)
            list_records_res_json = list_records_res.json()

            assert list_records_res.status_code == 200,  list_records_res.json()
            assert list_records_res_json.get("status") == "success"
            assert len(list_records_res_json.get("data")) == 1
            assert list_records_res_json.get("fetched_count") == 1
            assert list_records_res_json.get("has_more") is False
            if list_records_data.get("prefix_filter"):
                prefix_filter_dict = json.loads(list_records_data.get("prefix_filter"))
                for key in prefix_filter_dict:
                    assert list_records_res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))

    @pytest.mark.run(order=144)
    @pytest.mark.asyncio
    async def test_update_record(self):

        update_record_data_list = [
            {
                "type": "text",
                "content":
                    """Introduction
                      TaskingAI is an AI-native application development platform that unifies modules like Model,
                      Retrieval, Assistant, and Tool into one seamless ecosystem, streamlining the creation and
                      deployment of applications for developers.

                       Key Concepts
                       Project
                       Projects in TaskingAI are organizational units designed to group related activities and
                       resources. They offer a structured way to manage different initiatives or brands, allowing for
                       clear segregation and management. Each project can be tailored with specific config and
                       resources, ensuring that the information and activities within one project remain distinct and
                       isolated from others.

                       Model
                       TaskingAI incorporates a variety of chat completion models, each with distinct capabilities and
                       attributes. These models serve as the core 'brains' of AI assistants, providing them with
                       reasoning and logical capabilities. TaskingAI supports models from multiple providers, each
                       offering different strengths in terms of input token limits, reasoning, and logic capabilities.
                       Users can select and switch between models based on their specific needs and the complexity of
                       the tasks at hand.

                       Retrieval
                       Retrievals in TaskingAI are mechanisms that enable AI assistants to access and utilize external
                       knowledge bases. This feature allows the integration of additional information into the AI's
                       responses, enhancing its ability to provide accurate and context-relevant answers. Retrievals
                       are crucial for tasks that require specific, detailed, or up-to-date information, ensuring that
                       the AI's responses are not limited by its pre-training data.

                       Assistant
                       The Assistant feature in TaskingAI refers to the AI entities capable of performing a wide range
                       of tasks. These assistants are customizable and can be tailored to suit various applications,
                       from customer service to internal training. They operate based on the models and tools provided,
                       and their functionality can be extended through the use of retrievals, allowing them to access
                       a broader range of information and capabilities.

                       Tool
                       Tools in TaskingAI are functionalities that enable AI assistants to interact with external
                       resources and perform specific actions, such as fetching live information or communicating with
                       external systems. These tools are typically defined in OpenAPI schema format and can be attached
                       to assistants to enhance their capabilities. Tools are essential for tasks that require
                       real-time data or interaction with external APIs and services, making the assistants more
                       dynamic and versatile in their operation.

                       TaskingAI is more than just a platform; it's a gateway to unlocking the full potential of AI in
                       your daily tasks. Whether you're a developer, a researcher, or someone looking to streamline
                       their workflow, TaskingAI offers the tools and resources to achieve your goals.""",
                "text_splitter": {
                    "type": "token",
                    "chunk_size": 200,
                    "chunk_overlap": 100
                },

            },
            {
                "title": "test update record",
                "text_splitter": {
                    "type": "separator",
                    "separators": [",", "."],
                    "chunk_size": 100,
                    "chunk_overlap": 50
                }
            },
            {
                "metadata": {
                    "key1": "value1",
                    "key2": "value2"
                }
            }
        ]
        for update_record_data in update_record_data_list:
            res = await update_record(Retrieval.collection_id, Retrieval.record_id, update_record_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("record_id") == Retrieval.record_id
            assert res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert res_json.get("data").get("status") == "ready"

            for key in update_record_data:
                if key == "text_splitter":
                    continue
                else:
                    assert res_json.get("data").get(key) == update_record_data[key]

            get_res = await get_record(Retrieval.collection_id, Retrieval.record_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200, get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("record_id") == Retrieval.record_id
            assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
            assert get_res_json.get("data").get("status") == "ready"

            for key in update_record_data:
                if key == "text_splitter":
                    continue
                else:
                    assert get_res_json.get("data").get(key) == update_record_data[key]

    @pytest.mark.run(order=145)
    @pytest.mark.asyncio
    async def test_update_record_with_web(self):

        update_record_data = {
            "type": "web",
            # "title": "test create record with web",
            "url": "https://doc.adaprox.io/user-manuals/adfb0301-en",
            "text_splitter": {
                "type": "token",
                "chunk_size": 150,
                "chunk_overlap": 20
            }
        }

        res = await update_record(Retrieval.collection_id, Retrieval.record_id, update_record_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for key in update_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "url":
                assert update_record_data["url"] in res_json.get("data").get("content")
            else:
                assert res_json.get("data").get(key) == update_record_data[key]
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"

        record_id = res_json.get("data").get("record_id")

        get_res = await get_record(Retrieval.collection_id, record_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("record_id") == record_id
        assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert get_res_json.get("data").get("status") == "ready"

        for key in update_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "url":
                assert update_record_data["url"] in get_res_json.get("data").get("content")
            else:
                assert get_res_json.get("data").get(key) == update_record_data[key]

    @pytest.mark.run(order=145)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("upload_file_data", none_file_list)
    async def test_update_record_with_none_file(self, upload_file_data):

        res = await upload_file(upload_file_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        file_id = res.json()["data"]["file_id"]
        assert file_id is not None

        update_record_data = {
            "type": "file",
            "file_id": file_id,
            "text_splitter": {"type": "token", "chunk_size": 200, "chunk_overlap": 100}
        }

        res = await update_record(Retrieval.collection_id, Retrieval.record_id, update_record_data)
        res_json = res.json()
        assert res_json.get("status") == "error"

    @pytest.mark.run(order=146)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("upload_file_data", upload_file_list[2:3])
    async def test_update_record_with_file(self, upload_file_data):

        res = await upload_file(upload_file_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        file_id = res.json()["data"]["file_id"]
        assert file_id is not None

        update_record_data = {
            "type": "file",
            "file_id": file_id,
            "text_splitter": {"type": "token", "chunk_size": 200, "chunk_overlap": 100}
        }

        res = await update_record(Retrieval.collection_id, Retrieval.record_id, update_record_data)
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for key in update_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "file_id":
                content = json.loads(res_json.get("data").get("content"))
                assert content.get("file_id") == file_id
                assert content.get("file_name") == upload_file_data["file_name"]
                assert content.get("file_size") > 0
            else:
                assert res_json.get("data").get(key) == update_record_data[key]
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"

        record_id = res_json.get("data").get("record_id")

        get_res = await get_record(Retrieval.collection_id, record_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("record_id") == record_id
        assert get_res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert get_res_json.get("data").get("status") == "ready"

        for key in update_record_data:
            if key in ["text_splitter"]:
                continue
            elif key == "file_id":
                content = json.loads(res_json.get("data").get("content"))
                assert content.get("file_id") == file_id
                assert content.get("file_name") == upload_file_data["file_name"]
                assert content.get("file_size") > 0
            else:
                assert get_res_json.get("data").get(key) == update_record_data[key]
        # test file is exist
        await asyncio.sleep(1)
        res = await create_record(Retrieval.collection_id, update_record_data)
        res_json = res.json()
        assert res.status_code == 404, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "OBJECT_NOT_FOUND"

        update_record_data = {
            "type": "web",
            "url": "https://doc.adaprox.io/user-manuals/adfb0301-en",
            "text_splitter": {
                "type": "token",
                "chunk_size": 150,
                "chunk_overlap": 20
            }
        }

        res = await update_record(Retrieval.collection_id, Retrieval.record_id, update_record_data)
        res_json = res.json()

        assert res.status_code == 422, res.json()
        assert res_json.get("status") == "error"
        assert res_json.get("error").get("code") == "REQUEST_VALIDATION_ERROR"


    @pytest.mark.run(order=229)
    @pytest.mark.asyncio
    async def test_delete_record(self):

        records_res = await list_records(Retrieval.collection_id, {"limit": 100})
        record_ids = [record.get("record_id") for record in records_res.json().get("data")]
        for record_id in record_ids:

            res = await delete_record(Retrieval.collection_id, record_id)
            res_json = res.json()
            assert res.status_code == 200,  res.json()
            assert res_json.get("status") == "success"

            get_res = await get_record(Retrieval.collection_id, record_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 404, get_res.json()
            assert get_res_json.get("status") == "error"
            assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"

    @pytest.mark.run(order=220)
    @pytest.mark.asyncio
    async def test_record_and_chunk(self):

        if "WEB" in CONFIG.TEST_MODE:

            create_collection_dict = {
                "capacity": 1000,
                "embedding_model_id": CONFIG.text_embedding_model_id,
            }
            collection_res = await create_collection(create_collection_dict)
            collection_id = collection_res.json()["data"]["collection_id"]
            create_record_dict = {
                "text_splitter": {"type": "token", "chunk_size": 100,
                                  "chunk_overlap": 50},
                "content": """Introduction
                               TaskingAI is an AI-native application development platform that unifies modules like Model, Retrieval, Assistant, and Tool into one seamless ecosystem, streamlining the creation and deployment of applications for developers.
    
                                Key Concepts
                                Project
                                Projects in TaskingAI are organizational units designed to group related activities and resources. They offer a structured way to manage different initiatives or brands, allowing for clear segregation and management. Each project can be tailored with specific config and resources, ensuring that the information and activities within one project remain distinct and isolated from others.
    
                                Model
                                TaskingAI incorporates a variety of chat completion models, each with distinct capabilities and attributes. These models serve as the core 'brains' of AI assistants, providing them with reasoning and logical capabilities. TaskingAI supports models from multiple providers, each offering different strengths in terms of input token limits, reasoning, and logic capabilities. Users can select and switch between models based on their specific needs and the complexity of the tasks at hand.
    
                                Retrieval
                                Retrievals in TaskingAI are mechanisms that enable AI assistants to access and utilize external knowledge bases. This feature allows the integration of additional information into the AI's responses, enhancing its ability to provide accurate and context-relevant answers. Retrievals are crucial for tasks that require specific, detailed, or up-to-date information, ensuring that the AI's responses are not limited by its pre-training data.
    
                                Assistant
                                The Assistant feature in TaskingAI refers to the AI entities capable of performing a wide range of tasks. These assistants are customizable and can be tailored to suit various applications, from customer service to internal training. They operate based on the models and tools provided, and their functionality can be extended through the use of retrievals, allowing them to access a broader range of information and capabilities.
    
                                Tool
                                Tools in TaskingAI are functionalities that enable AI assistants to interact with external resources and perform specific actions, such as fetching live information or communicating with external systems. These tools are typically defined in OpenAPI schema format and can be attached to assistants to enhance their capabilities. Tools are essential for tasks that require real-time data or interaction with external APIs and services, making the assistants more dynamic and versatile in their operation.
    
                                TaskingAI is more than just a platform; it's a gateway to unlocking the full potential of AI in your daily tasks. Whether you're a developer, a researcher, or someone looking to streamline their workflow, TaskingAI offers the tools and resources to achieve your goals."""
            }
            record_res = await create_record(collection_id, create_record_dict)
            record_id = record_res.json()["data"]["record_id"]
            record_chunks = await list_record_chunks(collection_id, record_id, {"limit": 100})
            init_chunk_num = len(record_chunks.json()["data"])
            delete_chunks = record_chunks.json()["data"][:2]
            for chunk in delete_chunks:
                await delete_chunk(collection_id, chunk["chunk_id"])
            get_res = await get_record(collection_id, record_id)
            get_chunk_num = get_res.json()["data"]["num_chunks"]

            pytest.assume(get_chunk_num == init_chunk_num - 2)

            update_record_dict = {
                "title": "test update record",
                "content": """Introduction
                               TaskingAI is an AI-native application development platform that unifies modules like Model, Retrieval, Assistant, and Tool into one seamless ecosystem, streamlining the creation and deployment of applications for developers.
    
                                Key Concepts
                                Project
                                Projects in TaskingAI are organizational units designed to group related activities and resources. They offer a structured way to manage different initiatives or brands, allowing for clear segregation and management. Each project can be tailored with specific config and resources, ensuring that the information and activities within one project remain distinct and isolated from others.
    
                                Model
                                TaskingAI incorporates a variety of chat completion models, each with distinct capabilities and attributes. These models serve as the core 'brains' of AI assistants, providing them with reasoning and logical capabilities. TaskingAI supports models from multiple providers, each offering different strengths in terms of input token limits, reasoning, and logic capabilities. Users can select and switch between models based on their specific needs and the complexity of the tasks at hand.
    
                                Retrieval
                                Retrievals in TaskingAI are mechanisms that enable AI assistants to access and utilize external knowledge bases. This feature allows the integration of additional information into the AI's responses, enhancing its ability to provide accurate and context-relevant answers. Retrievals are crucial for tasks that require specific, detailed, or up-to-date information, ensuring that the AI's responses are not limited by its pre-training data.
    
                                Assistant
                                The Assistant feature in TaskingAI refers to the AI entities capable of performing a wide range of tasks. These assistants are customizable and can be tailored to suit various applications, from customer service to internal training. They operate based on the models and tools provided, and their functionality can be extended through the use of retrievals, allowing them to access a broader range of information and capabilities.
    
                                Tool
                                Tools in TaskingAI are functionalities that enable AI assistants to interact with external resources and perform specific actions, such as fetching live information or communicating with external systems. These tools are typically defined in OpenAPI schema format and can be attached to assistants to enhance their capabilities. Tools are essential for tasks that require real-time data or interaction with external APIs and services, making the assistants more dynamic and versatile in their operation.
    
                                TaskingAI is more than just a platform; it's a gateway to unlocking the full potential of AI in your daily tasks. Whether you're a developer, a researcher, or someone looking to streamline their workflow, TaskingAI offers the tools and resources to achieve your goals.""",
                "text_splitter": {
                    "type": "token",
                    "chunk_size": 50,
                    "chunk_overlap": 20
                },
                "metadata": {
                    "key": "value"
                }
            }
            update_record_res = await update_record(collection_id, record_id, update_record_dict)
            update_record_data = update_record_res.json()["data"]
            update_record_chunk_num = update_record_data["num_chunks"]

            pytest.assume(update_record_chunk_num != get_chunk_num)

            get_record_chunk = await list_record_chunks(collection_id, record_id, {"limit": 100})
            get_chunks = get_record_chunk.json()["data"]
            for chunk in get_chunks:
                await delete_chunk(collection_id, chunk["chunk_id"])
            get_collection_res = await get_collection(collection_id)
            get_collection_data = get_collection_res.json()["data"]
            get_collection_chunk_num = get_collection_data["num_chunks"]

            pytest.assume(get_collection_chunk_num == 0)

            delete_res = await delete_record(collection_id, record_id)
            get_collection_res = await get_collection(collection_id)
            get_collection_data = get_collection_res.json()["data"]
            get_collection_record_num = get_collection_data["num_records"]
            get_collection_chunk_num = get_collection_data["num_chunks"]

            pytest.assume(get_collection_record_num == 0)
            pytest.assume(get_collection_chunk_num == 0)

import pytest

from tests.services_api.retrieval.record import create_record, get_record, list_records, update_record, delete_record
from tests.services_tests.retrieval import Retrieval


class TestRecord(Retrieval):

    record_list = ["object", 'record_id', 'collection_id',  'num_chunks', 'content',  'metadata', 'type',
                   'updated_timestamp', 'created_timestamp', 'status', "title"]
    record_keys = set(record_list)

    @pytest.mark.run(order=35)
    @pytest.mark.asyncio
    async def test_create_record(self):

        create_record_data = {
            "type": "text",
            "title": "TaskingAI Introduction",
            "content":
                    """Introduction
                       TaskingAI is an AI-native application development platform that unifies modules like Model, Retrieval, Assistant, and Tool into one seamless ecosystem, streamlining the creation and deployment of applications for developers.
                        
                        Key Concepts
                        Project
                        Projects in TaskingAI are organizational units designed to group related activities and resources. They offer a structured way to manage different initiatives or brands, allowing for clear segregation and management. Each project can be tailored with specific settings and resources, ensuring that the information and activities within one project remain distinct and isolated from others.
                        
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
        }
        res = await create_record(Retrieval.collection_id, create_record_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        for key in create_record_data:
            if key == "text_splitter":
                continue
            else:
                assert res_json.get("data").get(key) == create_record_data[key]
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"
        assert set(res_json.get("data").keys()) == self.record_keys
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
        assert set(record_res_json.get("data").keys()) == self.record_keys

    @pytest.mark.run(order=37)
    @pytest.mark.asyncio
    async def test_list_records(self):
        list_records_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": Retrieval.record_id[:8]
        }
        list_records_res = await list_records(Retrieval.collection_id, list_records_data)
        list_records_res_json = list_records_res.json()
        assert list_records_res.status_code == 200
        assert list_records_res_json.get("status") == "success"
        assert len(list_records_res_json.get("data")) == 1
        assert list_records_res_json.get("fetched_count") == 1
        assert list_records_res_json.get("total_count") == 1
        assert list_records_res_json.get("has_more") is False

    @pytest.mark.run(order=38)
    @pytest.mark.asyncio
    async def test_update_record(self):
        update_record_data = {
             "type": "text",
             "title": "TaskingAI Introduction",
             "content":
                     """Introduction
                       TaskingAI is an AI-native application development platform that unifies modules like Model, 
                       Retrieval, Assistant, and Tool into one seamless ecosystem, streamlining the creation and 
                       deployment of applications for developers.
                        
                        Key Concepts
                        Project
                        Projects in TaskingAI are organizational units designed to group related activities and 
                        resources. They offer a structured way to manage different initiatives or brands, allowing for 
                        clear segregation and management. Each project can be tailored with specific settings and 
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
             "metadata": {
                "key1": "value1"
             }
        }
        res = await update_record(Retrieval.collection_id, Retrieval.record_id, update_record_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("record_id") == Retrieval.record_id
        assert res_json.get("data").get("collection_id") == Retrieval.collection_id
        assert res_json.get("data").get("status") == "ready"
        assert set(res_json.get("data").keys()) == self.record_keys
        for key in update_record_data:
            if key == "text_splitter":
                continue
            else:
                assert res_json.get("data").get(key) == update_record_data[key]

    @pytest.mark.run(order=49)
    @pytest.mark.asyncio
    async def test_delete_record(self):

        res = await delete_record(Retrieval.collection_id, Retrieval.record_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"

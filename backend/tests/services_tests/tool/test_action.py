import pytest
import json
from backend.tests.api_services.tool.action import (
    create_action,
    get_action,
    list_actions,
    update_action,
    delete_action,
    run_action,
)
from backend.tests.services_tests.tool import Tool
from backend.tests.common.utils import assume_action
from backend.tests.common.config import CONFIG

run_count = 0


@pytest.mark.api_test
class TestAction(Tool):

    create_action_data_list = [
        {
            "openapi_schema": {
                "openapi": "3.0.0",
                "info": {
                    "title": "OpenWeatherMap One Call API",
                    "description": "API for accessing comprehensive weather data from OpenWeatherMap.",
                    "version": "1.0.0",
                },
                "servers": [
                    {
                        "url": "https://api.openweathermap.org/data/3.0",
                        "description": "OpenWeatherMap One Call API server",
                    }
                ],
                "paths": {
                    "/onecall": {
                        "get": {
                            "summary": "Get Comprehensive Weather Data",
                            "description": "Retrieves weather data for a specific latitude and longitude.",
                            "operationId": "get_weather_data",
                            "parameters": [
                                {
                                    "in": "query",
                                    "name": "lat",
                                    "schema": {"type": "number", "format": "float", "minimum": -90, "maximum": 90},
                                    "required": True,
                                    "description": "Latitude, decimal (-90 to 90).",
                                },
                                {
                                    "in": "query",
                                    "name": "lon",
                                    "schema": {"type": "number", "format": "float", "minimum": -180, "maximum": 180},
                                    "required": True,
                                    "description": "Longitude, decimal (-180 to 180).",
                                },
                                {
                                    "in": "query",
                                    "name": "exclude",
                                    "schema": {"type": "string"},
                                    "required": False,
                                    "description": "Exclude some parts of the weather data "
                                    "(current, minutely, hourly, daily, alerts).",
                                },
                                {
                                    "in": "query",
                                    "name": "appid",
                                    "schema": {"type": "string", "enum": ["101f41d3ff4095824722d57a513cb80a"]},
                                    "required": True,
                                    "description": "Your unique API key.",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful response with comprehensive weather data.",
                                    "content": {"application/json": {"schema": {"type": "object", "properties": {}}}},
                                }
                            },
                        }
                    }
                },
            },
            "authentication": {"type": "none"},
        },
        {
            "openapi_schema": {
                "openapi": "3.0.0",
                "info": {
                    "title": "Numbers API",
                    "version": "1.0.0",
                    "description": "API for fetching interesting number facts",
                },
                "servers": [{"url": "http://numbersapi.com"}],
                "paths": {
                    "/{number}": {
                        "get": {
                            "description": "Get fact about a number",
                            "operationId": "get_number_fact",
                            "parameters": [
                                {
                                    "name": "number",
                                    "in": "path",
                                    "required": True,
                                    "description": "The number to get the fact for",
                                    "schema": {"type": "integer"},
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "A fact about the number",
                                    "content": {"text/plain": {"schema": {"type": "string"}}},
                                }
                            },
                        }
                    }
                },
            },
            "authentication": {"type": "none"},
        },
        {
            "openapi_schema": {
                "openapi": "3.1.0",
                "info": {
                    "title": "Get weather data",
                    "description": "Retrieves current weather data for a location.",
                    "version": "v1.0.0",
                },
                "servers": [{"url": "https://weather.example.com"}],
                "paths": {
                    "/location": {
                        "get": {
                            "description": "Get temperature for a specific location 123",
                            "operationId": "GetCurrentWeather123",
                            "parameters": [
                                {
                                    "name": "location",
                                    "in": "query",
                                    "description": "The city and state to retrieve the weather for",
                                    "required": True,
                                    "schema": {"type": "string"},
                                }
                            ],
                            "deprecated": False,
                        }
                    }
                },
                "components": {"schemas": {}},
            },
            "authentication": {"type": "bearer", "secret": "ASD213dfslkfa12"},
        },
        {
            "openapi_schema": {
                "openapi": "3.1.0",
                "info": {
                    "title": "Get weather data",
                    "description": "Retrieves current weather data for a location.",
                    "version": "v1.0.0",
                },
                "servers": [{"url": "https://weather.example.com"}],
                "paths": {
                    "/location": {
                        "get": {
                            "description": "Get temperature for a specific location",
                            "operationId": "GetCurrentWeather",
                            "parameters": [
                                {
                                    "name": "location",
                                    "in": "query",
                                    "description": "The city and state to retrieve the weather for",
                                    "required": True,
                                    "schema": {"type": "string"},
                                }
                            ],
                            "deprecated": False,
                        }
                    }
                },
                "components": {"schemas": {}},
            },
            "authentication": {"type": "custom", "content": {"apikey": "123456789"}},
        },
    ]
    run_action_data_list = [{"parameters": {"number": 42}}, {"parameters": {"lon": 120.1552, "lat": 30.2741}}]
    action_ids = []
    action_names = []

    @pytest.mark.run(order=161)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("create_action_data", create_action_data_list)
    async def test_create_action(self, create_action_data):

        res = await create_action(create_action_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        for action in res_json.get("data"):

            assume_action(res_json.get("data")[0], create_action_data)
            TestAction.action_ids.append(action.get("action_id"))
            TestAction.action_names.append(action.get("name"))
            Tool.action_id = action.get("action_id")

            get_res = await get_action(Tool.action_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200, get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("action_id") == Tool.action_id

            assume_action(get_res_json.get("data"), create_action_data)


    @pytest.mark.run(order=162)
    @pytest.mark.asyncio
    async def test_list_actions(self):



        list_action_data_list = [
            {"limit": 10, "order": "desc", "after": TestAction.action_ids[1]},
            {"limit": 10, "order": "asc", "prefix_filter": json.dumps({"name": TestAction.action_names[1][:8]})},
            {
                "limit": 10,
                "order": "desc",
                "prefix_filter": json.dumps({"action_id": TestAction.action_ids[1][:14]}),
            },
        ]
        for list_actions_data in list_action_data_list:
            if "API" in CONFIG.TEST_MODE:
                if list_actions_data.get("prefix_filter"):
                    continue
            res = await list_actions(list_actions_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert len(res_json.get("data")) == 1
            assert res_json.get("fetched_count") == 1
            assert res_json.get("has_more") is False
            if list_actions_data.get("prefix_filter"):
                prefix_filter_dict = json.loads(list_actions_data.get("prefix_filter"))
                for key in prefix_filter_dict:
                    assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))


    @pytest.mark.run(order=163)
    @pytest.mark.asyncio
    async def test_get_action(self):


        res = await get_action(TestAction.action_ids[0])
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("action_id") == TestAction.action_ids[0]


    @pytest.mark.run(order=164)
    @pytest.mark.asyncio
    async def test_run_action(self):

        run_res = await run_action(TestAction.action_ids[1], TestAction.run_action_data_list[0])

        run_res_json = run_res.json()
        assert run_res.status_code == 200, run_res.json()
        assert run_res_json.get("status") == "success"
        assert run_res_json.get("data").get("status") == 200


    @pytest.mark.run(order=165)
    @pytest.mark.asyncio
    async def test_update_action(self):

        update_action_data_list = [
            {
                "openapi_schema": {
                    "openapi": "3.1.0",
                    "info": {
                        "title": "Get weather data",
                        "description": "Retrieves current weather data for a location.",
                        "version": "v1.0.0",
                    },
                    "servers": [{"url": "https://weather.example.com"}],
                    "paths": {
                        "/location": {
                            "get": {
                                "description": "Get temperature for a specific location 123",
                                "operationId": "GetCurrentWeather123",
                                "parameters": [
                                    {
                                        "name": "location",
                                        "in": "query",
                                        "description": "The city and state to retrieve the weather for",
                                        "required": True,
                                        "schema": {"type": "string"},
                                    }
                                ],
                                "deprecated": False,
                            }
                        }
                    },
                    "components": {"schemas": {}},
                },
                "authentication": {"type": "bearer", "secret": "ASD213dfslkfa12"},
            },
            {
                "openapi_schema": {
                    "openapi": "3.1.0",
                    "info": {
                        "title": "Get weather data",
                        "description": "Retrieves current weather data for a location.",
                        "version": "v1.0.0",
                    },
                    "servers": [{"url": "https://weather.example.com"}],
                    "paths": {
                        "/location": {
                            "get": {
                                "description": "Get temperature for a specific location",
                                "operationId": "GetCurrentWeather",
                                "parameters": [
                                    {
                                        "name": "location",
                                        "in": "query",
                                        "description": "The city and state to retrieve the weather for",
                                        "required": True,
                                        "schema": {"type": "string"},
                                    }
                                ],
                                "deprecated": False,
                            }
                        }
                    },
                    "components": {"schemas": {}},
                },
                "authentication": {"type": "custom", "content": {"apikey": "123456789"}},
            },
        ]

        for update_action_data in update_action_data_list:
            res = await update_action(TestAction.action_ids[0], update_action_data)

            res_json = res.json()
            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert res_json.get("data").get("action_id") == TestAction.action_ids[0]

            assume_action(res_json.get("data"), update_action_data)

            get_res = await get_action(TestAction.action_ids[0])
            get_res_json = get_res.json()
            assert get_res.status_code == 200, get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("action_id") == TestAction.action_ids[0]

            assume_action(get_res_json.get("data"), update_action_data)


    @pytest.mark.run(order=230)
    @pytest.mark.asyncio
    async def test_delete_action(self):

        actions = await list_actions({})
        action_ids = [action.get("action_id") for action in actions.json().get("data")]
        for action_id in action_ids:
            res = await delete_action(action_id)
            res_json = res.json()
            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"

            get_res = await get_action(action_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 404, get_res.json()
            assert get_res_json.get("status") == "error"
            assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"

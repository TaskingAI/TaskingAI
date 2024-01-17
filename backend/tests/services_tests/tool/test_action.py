import pytest

from tests.services_api.tool.action import (create_action, get_action, list_actions, update_action, delete_action,
                                            run_action)


run_count = 0


class TestAction:

    action_list = ['object', 'action_id', 'name', 'description', 'authentication', 'openapi_schema',
                   'created_timestamp', 'updated_timestamp']
    action_keys = set(action_list)
    action_authentication = ['type', 'secret', 'content']
    action_authentication_keys = set(action_authentication)
    action_openapi_schema = ['openapi', 'info', 'servers', 'paths', 'components', 'security']
    action_openapi_schema_keys = set(action_openapi_schema)

    create_action_data_list = [
        {
                        "openapi_schema": {
                            "openapi": "3.0.0",
                            "info": {
                                "title": "Numbers API",
                                "version": "1.0.0",
                                "description": "API for fetching interesting number facts"
                            },
                            "servers": [
                                {
                                    "url": "http://numbersapi.com"
                                }
                            ],
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
                                                "schema": {
                                                    "type": "integer"
                                                }
                                                 }
                                                 ],
                                        "responses": {
                                                    "200": {
                                                        "description": "A fact about the number",
                                                        "content": {
                                                            "text/plain": {
                                                                "schema": {
                                                                    "type": "string"
                                                                }
                                                                    }
                                                                    }
                                                                    }
                                                                    }
                                                                    }
                                }
                            }
                            }
                    },
        {
            "openapi_schema": {
                "openapi": "3.0.0",
                "info": {
                    "title": "OpenWeatherMap One Call API",
                    "description": "API for accessing comprehensive weather data from OpenWeatherMap.",
                    "version": "1.0.0"
                },
                "servers": [
                    {
                        "url": "https://api.openweathermap.org/data/3.0",
                        "description": "OpenWeatherMap One Call API server"
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
                                    "schema": {
                                        "type": "number",
                                        "format": "float",
                                        "minimum": -90,
                                        "maximum": 90
                                    },
                                    "required": True,
                                    "description": "Latitude, decimal (-90 to 90)."
                                },
                                {
                                    "in": "query",
                                    "name": "lon",
                                    "schema": {
                                        "type": "number",
                                        "format": "float",
                                        "minimum": -180,
                                        "maximum": 180
                                    },
                                    "required": True,
                                    "description": "Longitude, decimal (-180 to 180)."
                                },
                                {
                                    "in": "query",
                                    "name": "exclude",
                                    "schema": {
                                        "type": "string"
                                    },
                                    "required": False,
                                    "description": "Exclude some parts of the weather data "
                                                   "(current, minutely, hourly, daily, alerts)."
                                },
                                {
                                    "in": "query",
                                    "name": "appid",
                                    "schema": {
                                        "type": "string",
                                        "enum": ["101f41d3ff4095824722d57a513cb80a"]
                                    },
                                    "required": True,
                                    "description": "Your unique API key."
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful response with comprehensive weather data.",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "openapi_schema": {
                "openapi": "3.0.0",
                "info": {
                    "title": "OpenAI Chat API",
                    "version": "1.0.0",
                    "description": "API for interacting with OpenAI's chat model."
                },
                "servers": [
                    {
                        "url": "https://api.openai.com/v1"
                    }
                ],
                "paths": {
                    "/chat/completions": {
                        "post": {
                                    "summary": "Creates a model response for the given chat conversation.",
                                    "description": "Creates a model response for the given chat conversation.",
                                    "operationId": "createChatCompletion",
                                    "tags": [
                                        "chat"
                                    ],
                                    "requestBody": {
                                        "required": True,
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "type": "object",
                                                    "properties": {
                                                        "model": {
                                                            "type": "string",
                                                            "description": "ID of the model to use."
                                                        },
                                                        "messages": {
                                                            "type": "array",
                                                            "description": "A list of messages comprising the"
                                                                           " conversation so far."
                                                        },
                                                        "function_call": {
                                                            "type": "string",
                                                            "enum": ["auto"]
                                                        }
                                                    },
                                                    "required": [
                                                        "model",
                                                        "messages"
                                                    ]
                                                }
                                            }
                                        }
                                    },
                                    "responses": {
                                        "200": {
                                            "description": "A successful response.",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    }
                                    }
                                    }
                                    },
                "authentication": {
                    "type": "bearer",
                    "secret": "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"
                }
                }
    ]
    run_action_data_list = [
        {
            "parameters": {
                "number": 42
            }
        },
        {
            "parameters": {
                "lon": 120.1552,
                "lat": 30.2741
            }
        },
        {
            "parameters": {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": "Hello!"
                    }
                ]
            }
        }
        ]
    action_ids = []
    action_names = []

    @pytest.mark.run(order=31)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("create_action_data", create_action_data_list)
    async def test_create_action(self, create_action_data):

        res = await create_action(create_action_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        for action in res_json.get("data"):
            assert set(action.keys()) == TestAction.action_keys
            assert set(action.get("authentication").keys()).issubset(TestAction.action_authentication_keys)
            assert set(action.get("openapi_schema").keys()) == TestAction.action_openapi_schema_keys
            TestAction.action_ids.append(action.get("action_id"))
            TestAction.action_names.append(action.get("name"))

    @pytest.mark.run(order=32)
    @pytest.mark.asyncio
    async def test_list_actions(self):

        list_actions_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": TestAction.action_ids[0][:14],
            "name_search": TestAction.action_names[0][:4],
        }
        res = await list_actions(list_actions_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == 1
        assert res_json.get("fetched_count") == 1
        assert res_json.get("total_count") == 1
        assert res_json.get("has_more") is False

    @pytest.mark.run(order=33)
    @pytest.mark.asyncio
    async def test_get_action(self):

        res = await get_action(TestAction.action_ids[0])
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("action_id") == TestAction.action_ids[0]
        assert set(res_json.get("data").keys()) == TestAction.action_keys
        assert set(res_json.get("data").get("authentication").keys()).issubset(TestAction.action_authentication_keys)
        assert set(res_json.get("data").get("openapi_schema").keys()).issubset(TestAction.action_openapi_schema_keys)

    @pytest.mark.run(order=34)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("run_action_data", run_action_data_list)
    async def test_run_action(self, run_action_data):

        global run_count
        run_res = await run_action(TestAction.action_ids[run_count], run_action_data)
        run_res_json = run_res.json()
        assert run_res.status_code == 200
        assert run_res_json.get("status") == "success"
        assert run_res_json.get("data").get("status") == 200
        run_count += 1

    @pytest.mark.run(order=35)
    @pytest.mark.asyncio
    async def test_update_action(self):

        update_action_data = {
                                "openapi_schema": {
                                    "openapi": "3.1.0",
                                    "info": {
                                        "title": "Get weather data",
                                        "description": "Retrieves current weather data for a location.",
                                        "version": "v1.0.0"
                                    },
                                    "servers": [
                                        {
                                            "url": "https://weather.example.com"
                                        }
                                    ],
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
                                                        "schema": {
                                                            "type": "string"
                                                        }
                                                    }
                                                ],
                                                "deprecated": False
                                            }
                                        }
                                    },
                                    "components": {
                                        "schemas": {}
                                    }
                                },
                                "authentication": {
                                    "type": "bearer",
                                    "secret": "ASD213dfslkfa12"
                                }
                            }
        res = await update_action(TestAction.action_ids[0], update_action_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("action_id") == TestAction.action_ids[0]
        assert set(res_json.get("data").keys()) == TestAction.action_keys
        assert set(res_json.get("data").get("authentication").keys()).issubset(TestAction.action_authentication_keys)
        assert set(res_json.get("data").get("openapi_schema").keys()).issubset(TestAction.action_openapi_schema_keys)

    @pytest.mark.run(order=36)
    @pytest.mark.asyncio
    async def test_delete_action(self):

        for action_id in TestAction.action_ids:
            res = await delete_action(action_id)
            res_json = res.json()
            assert res.status_code == 200
            assert res_json.get("status") == "success"

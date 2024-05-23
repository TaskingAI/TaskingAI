import pytest
import json
import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict
import random
import string
import os
import aiohttp
from backend.tests.common.logger import logger


class ResponseWrapper:
    def __init__(self, status: int, json_data: Dict):
        self.status_code = status
        self._json_data = json_data

    def json(self):
        return self._json_data


def list_to_dict(data: list):
    d = {}
    for i in data:
        if isinstance(i, dict):
            for k, v in i.items():
                d[k] = v
        else:
            d.update(i)
    return d


def get_headers(authentication: str):
    return {"Authorization": "Bearer " + authentication}


def assume_text_embedding_result(result: list):
    pytest.assume(len(result) > 0)
    pytest.assume(all(isinstance(value, float) for value in result))


def assume_collection_result(create_dict: dict, res_dict: dict):
    for key in create_dict:
        pytest.assume(res_dict[key] == create_dict[key])
    pytest.assume(res_dict["status"] == "ready")


def assume_record_result(create_record_data: dict, res_dict: dict):
    for key in create_record_data:
        if key == "text_splitter":
            continue
        pytest.assume(res_dict[key] == create_record_data[key])
    pytest.assume(res_dict["status"] == "ready")


def assume_chunk_result(chunk_dict: dict, res: dict):
    for key, value in chunk_dict.items():
        pytest.assume(res[key] == chunk_dict[key])


def assume_query_chunk_result(query_text, chunk_dict: dict):
    pytest.assume(query_text in chunk_dict["content"])
    pytest.assume(isinstance(chunk_dict["score"], float))


def assume_assistant_result(assistant_dict: dict, res: dict):
    for key, value in assistant_dict.items():
        if key == "error":
            continue
        elif key == "system_prompt_template" and isinstance(value, str):
            pytest.assume(res[key] == [assistant_dict[key]])
        elif key in ["memory", "tool", "retrievals"]:
            continue
        else:
            pytest.assume(res[key] == assistant_dict[key])


def assume_chat_result(chat_dict: dict, res: dict):
    for key, value in chat_dict.items():
        if key == "error":
            continue
        else:
            pytest.assume(res[key] == chat_dict[key])


def assume_message_result(message_dict: dict, res: dict):
    for key, value in message_dict.items():
        if key == "error":
            continue
        else:
            pytest.assume(res[key] == message_dict[key])


def assume(res, except_dict: Dict):
    pytest.assume(res.status_code == int(except_dict["except_http_code"]), res.json())
    pytest.assume(res.json()["status"] == except_dict["except_status"])


def assume_success(res, except_dict: Dict):
    assume(res, except_dict)
    pytest.assume(res.json()["data"]["status"] == except_dict["except_data_status"])


def assume_error(res, except_dict: Dict):
    assume(res, except_dict)
    pytest.assume(res.json()["error"]["code"] == except_dict["except_error_code"])


def assume_auth(res, auth_dict: Dict):
    for key, value in auth_dict.items():
        if key == "password" or "new_password" or "verification_code":
            continue
        else:
            pytest.assume(res.json()["data"][key] == auth_dict[key])


def get_password():
    return "".join(random.choices(string.ascii_letters, k=7)) + str(random.randint(0, 9))


def assume_user_profile(res, user_dict: Dict):
    for key, value in user_dict.items():
        pytest.assume(res.json()["data"][key] == user_dict[key])


def assume_space(res, space_dict: Dict):
    for key, value in space_dict.items():
        pytest.assume(res.json()["data"][key] == space_dict[key])


def assume_count(res, except_dict: Dict):
    assume(res, except_dict)
    pytest.assume(len(res.json()["data"]) >= 0)
    pytest.assume(res.json()["fetched_count"] >= 0)
    pytest.assume(len(res.json()["data"]) == res.json()["fetched_count"])


def assume_project(res, project_dict: Dict):
    for key, value in project_dict.items():
        pytest.assume(res.json()["data"][key] == project_dict[key])


def assume_bundle_instance(bundle_instance, bundle_instance_dict: Dict):
    for key, value in bundle_instance_dict.items():
        if key == "credentials":
            continue
        else:
            pytest.assume(bundle_instance[key] == bundle_instance_dict[key])


def load_str_env(name: str, required: bool = False) -> str:
    """
    Load environment variable as string
    :param name: name of the environment variable
    :param required: whether the environment variable is required
    """
    if os.environ.get(name):
        return os.environ.get(name)

    if required:
        raise Exception(f"Env {name} is not set")


def assume_model(res, model_dict: Dict):
    for key, value in model_dict.items():
        if key == "max_count":
            pass
        elif key == "credentials":
            for k, v in value.items():
                if "API_KEY" in k:
                    pytest.assume("*" in res.json()["data"]["display_credentials"][k])
                else:
                    pytest.assume(res.json()["data"]["display_credentials"][k] == model_dict["credentials"][k])
        elif key == "properties":
            for k, v in value.items():
                pytest.assume(res.json()["data"][key][k] == model_dict[key][k])
        else:
            pytest.assume(res.json()["data"][key] == model_dict[key])


def assume_action(action, action_dict: Dict):
    for key, value in action_dict.items():
        if key == "max_count":
            continue
        elif key == "openapi_schema":
            for k, v in value.items():
                if k == "components":
                    continue
                elif k == "paths":
                    for i in action[key][k]:
                        pytest.assume(action[key][k][i] == action_dict[key][k][i])
                else:
                    pytest.assume(action[key][k] == action_dict[key][k])
        elif key == "authentication":
            no_none_action = {}
            for k, v in value.items():
                if k == "type":
                    pytest.assume(action[key][k] == action_dict[key][k])
            #     if v is not None or k != "encrypted":
            #         no_none_action[k] = v
            # # no_none_action = {k: v for k, v in action[key].items() if v is not None or k != "encrypted"}
            # no_none_action_dict = {k: v for k, v in action_dict[key].items() if v is not None}
            # if not (no_none_action == no_none_action_dict):
            #     print(f"assume_action: action[{key}]={action[key]}, action_dict[{key}] ={action_dict[key]}, "
            #           f"action[key] == action_dict[key] = {action[key] == action_dict[key]}")
            # pytest.assume(no_none_action == no_none_action_dict)
        else:
            if not (action[key] == action_dict[key]):
                print(
                    f"assume_action: action[{key}]={action[key]}, action_dict[{key}] ={action_dict[key]}, "
                    f"action[key] == action_dict[key] = {action[key] == action_dict[key]}"
                )
            pytest.assume(action[key] == action_dict[key])


def generate_random_string(length):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def get_file_name(file_path: str):
    return file_path.split("/")[-1]


SSE_DONE_MSG = "data: [DONE]\n\n"


async def sse_stream(
    token: str,
    url: str,
    payload: Dict,
):
    headers = get_headers(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=payload) as response:
            buffer = ""
            # handle streaming response in different json chunks
            async for line in response.content:
                if line.endswith(b"\n"):
                    buffer += line.decode()
                    if buffer.endswith("\n\n"):
                        lines = buffer.strip().split("\n")
                        event_data = lines[0][len("data: ") :]
                        if event_data != "[DONE]":
                            try:
                                data = json.loads(event_data)
                                yield data
                            except json.decoder.JSONDecodeError:
                                logger.error(f"Failed to parse json: {event_data}")
                                continue
                        buffer = ""


def check_order(lst, key):
    return all(lst[i][key] >= lst[i + 1][key] for i in range(len(lst) - 1))

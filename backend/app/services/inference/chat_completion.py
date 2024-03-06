import aiohttp
from typing import List, Dict, Optional
from tkhelper.utils import ResponseWrapper
from app.config import CONFIG
import json
import logging

logger = logging.getLogger(__name__)


__all__ = [
    "chat_completion",
    "chat_completion_stream",
]


# For POST /v1/chat_completion
async def chat_completion(
    model_schema_id: str,
    provider_model_id: Optional[str],
    messages: List[Dict],
    encrypted_credentials: Dict,
    properties: Optional[Dict],
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
) -> ResponseWrapper:
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "encrypted_credentials": encrypted_credentials,
        "properties": properties,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": False,
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def chat_completion_stream(
    model_schema_id: str,
    provider_model_id: Optional[str],
    messages: List[Dict],
    encrypted_credentials: Dict,
    properties: Optional[Dict],
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
):
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "encrypted_credentials": encrypted_credentials,
        "properties": properties,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": True,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(request_url, json=payload) as response:
            buffer = ""
            async for line in response.content:
                if line.endswith(b"\n"):
                    buffer += line.decode()
                    if buffer.endswith("\n\n"):
                        lines = buffer.strip().split("\n")
                        event_data = lines[0][len("data: ") :]
                        try:
                            data = json.loads(event_data)
                            yield data
                        except json.decoder.JSONDecodeError:
                            print("JSONDecodeError")
                            continue
                        buffer = ""

import aiohttp
from typing import List, Dict, Optional
from common.utils import ResponseWrapper
from config import CONFIG

import json
import logging

logger = logging.getLogger(__name__)


async def chat_completion(
    provider_id: str,
    provider_model_id: str,
    messages: List[Dict],
    credentials: Dict,
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
) -> ResponseWrapper:
    payload = {
        "provider_id": provider_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "encrypted_credentials": credentials,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": False,
    }

    async with aiohttp.ClientSession() as session:
        request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
        response = await session.post(request_url, json=payload)
        return ResponseWrapper(response.status, await response.json())


async def chat_completion_stream(
    provider_id: str,
    provider_model_id: str,
    messages: List[Dict],
    credentials: Dict,
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
):
    payload = {
        "provider_id": provider_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "credentials": credentials,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": True,
    }

    async with aiohttp.ClientSession() as session:
        request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
        async with session.post(request_url, json=payload) as response:
            buffer = ""
            # handle streaming response in different json chunks
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
                            logger.error(f"chat_completion_stream: Failed to decode json: {event_data}")
                            continue
                        buffer = ""

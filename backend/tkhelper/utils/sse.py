from starlette.responses import StreamingResponse
from fastapi import HTTPException
from typing import Dict, Callable, Coroutine, Any
import json
import aiohttp
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "sse_stream",
    "SSE_DONE_MSG",
    "sse_stream_response",
    "sse_stream_dict_generate",
]


SSE_DONE_MSG = "data: [DONE]\n\n"


async def sse_stream(url: str, payload: Dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                content = await response.json()
                raise HTTPException(status_code=response.status, detail=content.get("error", {}))

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


async def sse_stream_response(
    sse_generator,
    chunk_handler: Callable[[Dict], Coroutine[Any, Any, None]] = None,
):
    # raise error in the first response if needed
    first_chunk = await sse_generator.__anext__()

    if first_chunk is not None and first_chunk.get("object", "").lower() == "error":
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": first_chunk.get("code", "UNKNOWN_ERROR"),
                "message": first_chunk.get("message", "Unknown error"),
            },
        )

    async def generator(first_chunk, sse_generator, chunk_handler):
        # handle the first chunk if it is a chat completion object
        if chunk_handler is not None:
            await chunk_handler(first_chunk)
        # yield first chunk if it is not an error chunk
        yield f"data: {json.dumps(first_chunk)}\n\n"

        async for response_dict in sse_generator:
            # remove empty values
            response_dict = {k: v for k, v in response_dict.items() if v is not None}
            if chunk_handler is not None:
                await chunk_handler(response_dict)
            yield f"data: {json.dumps(response_dict)}\n\n"

        yield SSE_DONE_MSG

    return StreamingResponse(
        generator(
            first_chunk=first_chunk,
            sse_generator=sse_generator,
            chunk_handler=chunk_handler,
        ),
        media_type="text/event-stream",
    )


async def sse_stream_dict_generate(
    url: str,
    payload: Dict,
    chunk_handler: Callable[[Dict], Coroutine[Any, Any, None]] = None,
):
    sse_generator = sse_stream(url, payload)

    # raise error in the first response if needed
    first_chunk = await sse_generator.__anext__()

    if first_chunk is not None and first_chunk.get("object", "").lower() == "error":
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": first_chunk.get("code", "UNKNOWN_ERROR"),
                "message": first_chunk.get("message", "Unknown error"),
            },
        )

    async def generator(first_chunk, sse_generator, chunk_handler):
        # handle the first chunk if it is a chat completion object
        if chunk_handler is not None:
            await chunk_handler(first_chunk)
        # yield first chunk if it is not an error chunk
        yield first_chunk

        async for response_dict in sse_generator:
            # remove empty values
            response_dict = {k: v for k, v in response_dict.items() if v is not None}
            if chunk_handler is not None:
                await chunk_handler(response_dict)
            yield response_dict

    return generator(
        first_chunk=first_chunk,
        sse_generator=sse_generator,
        chunk_handler=chunk_handler,
    )

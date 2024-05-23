from __future__ import annotations
import json
from typing import Any, Dict, Iterator, AsyncIterator, Optional
import logging

logger = logging.getLogger(__name__)

__all__ = ["AsyncStream", "ServerSentEvent", "SSEDecoder"]


class AsyncStream(object):
    """Provides the core interface to iterate over an asynchronous stream response."""

    def __init__(self, async_stream_generator):
        self._async_stream_generator = async_stream_generator
        self._decoder = SSEDecoder()  # Assuming SSEDecoder is compatible with async
        self._iterator = self.__stream__()

    async def __anext__(self) -> Dict:
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[Dict]:
        async for item in self._iterator:
            yield item

    async def _iter_events(self) -> AsyncIterator[str]:
        # Decode binary data to strings before passing it to the SSE decoder.
        async for chunk in self._async_stream_generator:
            if isinstance(chunk, bytes):
                # Decode the binary data to a string, assuming UTF-8 encoding.
                decoded_chunk = chunk.decode("utf-8")
                # Yield each decoded line to the SSE decoder as if they were SSE events.
                for line in decoded_chunk.split("\n"):
                    if line:  # Skip empty lines
                        yield line
            else:
                # Directly yield the chunk if it's not bytes, assuming it's already a string.
                # This condition might never be true, but it's here for completeness.
                yield chunk

    async def __stream__(self) -> AsyncIterator[Dict]:
        async for sse_line in self._iter_events():

            # skip the line with [DONE] as it indicates the end of the stream
            if "[DONE]" in sse_line:
                break

            # Check if the line starts with "data: " which indicates SSE data field
            if sse_line.startswith("data:"):
                try:
                    # Extract JSON data from the SSE data field
                    data_str = sse_line[len("data:") :]  # Remove the "data: " prefix
                    data = json.loads(data_str)  # Parse the JSON data
                    yield data
                except json.JSONDecodeError as e:
                    logger.debug(f"Failed to parse JSON data: {e}")
                    continue  # Skip this line and continue with the next
            elif sse_line.strip():
                try:
                    # Extract JSON data from the SSE data field
                    data = json.loads(sse_line)  # Parse the JSON data
                    yield data
                except json.JSONDecodeError as e:
                    logger.debug(f"Failed to parse JSON data: {e}")
                    continue  # Skip this line and continue with the next

        # Ensure the entire stream is consumed
        async for _ in self._iter_events():
            pass  # No operation, just consuming the rest of the stream if needed


class ServerSentEvent:
    def __init__(
        self,
        *,
        event: Optional[str] = None,
        data: Optional[str] = None,
        id: Optional[str] = None,
        retry: Optional[int] = None,
    ) -> None:
        if data is None:
            data = ""

        self._id = id
        self._data = data
        self._event = event or None
        self._retry = retry

    @property
    def event(self) -> Optional[str]:
        return self._event

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def retry(self) -> Optional[int]:
        return self._retry

    @property
    def data(self) -> str:
        return self._data

    def json(self) -> Any:
        return json.loads(self.data)

    def __repr__(self) -> str:
        return f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id}, retry={self.retry})"


class SSEDecoder:
    _data: list[str]
    _event: Optional[str]
    _retry: Optional[int]
    _last_event_id: Optional[str]

    def __init__(self) -> None:
        self._event = None
        self._data = []
        self._last_event_id = None
        self._retry = None

    def iter(self, iterator: Iterator[str]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields lines, iterate over it & yield every event encountered"""
        for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    async def aiter(self, iterator: AsyncIterator[str]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        async for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    def decode(self, line: str) -> Optional[ServerSentEvent]:
        # See: https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation  # noqa: E501

        if not line:
            if not self._event and not self._data and not self._last_event_id and self._retry is None:
                return None

            sse = ServerSentEvent(
                event=self._event,
                data="\n".join(self._data),
                id=self._last_event_id,
                retry=self._retry,
            )

            # NOTE: as per the SSE spec, do not reset last_event_id.
            self._event = None
            self._data = []
            self._retry = None

            return sse

        if line.startswith(":"):
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            value = value[1:]

        if fieldname == "event":
            self._event = value
        elif fieldname == "data":
            self._data.append(value)
        elif fieldname == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif fieldname == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass
        else:
            pass  # Field is ignored.

        return None

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from aiohttp import ClientTimeout

from tkhelper.error import raise_http_error, ErrorCode
from .base import BaseFileLoader


class WebContentLoader(BaseFileLoader):
    async def read_content(self, url, timeout_seconds=10):  # Default timeout set to 10 seconds
        # Define the timeout
        timeout = ClientTimeout(total=timeout_seconds)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url=url) as response:
                    if response.status != 200:
                        raise_http_error(
                            ErrorCode.INVALID_REQUEST,  # Adjust error code as needed
                            f"Failed to load the web content with status code {response.status}.",
                        )

                    try:
                        data = await response.text()
                    except UnicodeDecodeError as e:
                        # Raise an error if text cannot be decoded
                        raise_http_error(
                            ErrorCode.INVALID_REQUEST,
                            f"Failed to load the web content because the content is not UTF-8 encoded.",
                        )

                    soup = BeautifulSoup(data, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)

                    return text

        except asyncio.TimeoutError:
            raise_http_error(
                ErrorCode.INVALID_REQUEST,
                f"Failed to load the web content due to timeout error.",
            )
        except aiohttp.ClientError as e:
            raise_http_error(
                ErrorCode.INVALID_REQUEST,
                f"Failed to load the web content due to network error.",
            )

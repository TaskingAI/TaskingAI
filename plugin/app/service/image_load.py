import base64
from io import BytesIO

import aiohttp

from app.error import raise_http_error, ErrorCode, raise_provider_api_error
from config import CONFIG

from PIL import Image

def image_url_is_on_localhost(url):
    local_url_identifiers = ['localhost', '0.0.0.0', '127.0.0.1', '::1']

    if any(item in url for item in local_url_identifiers):
        if "/imgs/" not in url:
            raise_http_error(ErrorCode.PROVIDER_ERROR, "Invalid local image url.")
        return True

    return False

async def fetch_image_format(url):

    # Image in local file system
    if image_url_is_on_localhost(url):

        local_file_path = CONFIG.PATH_TO_VOLUME + "/imgs/" + url.split("/imgs/")[1]
        with open(local_file_path, "rb") as image_file:
            image_bytes = image_file.read()
            image = Image.open(BytesIO(image_bytes))
            return image.format

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()  # Ensure the request was successful
            # Read the response content as bytes
            image_bytes = await response.read()
            # Load the image into a PIL Image object
            image = Image.open(BytesIO(image_bytes))
            # Output the format of the image
            return image.format

async def get_image_base64_string(image_uri):

    # Image in local file system
    if image_url_is_on_localhost(image_uri):
        local_file_path = CONFIG.PATH_TO_VOLUME + "/imgs/" + image_uri.split("/imgs/")[1]

        with open(local_file_path, "rb") as image_file:
            image_bytes = image_file.read()
            base64_string = base64.b64encode(image_bytes).decode("utf-8")
            return base64_string

    # Normal url
    async with aiohttp.ClientSession() as session:
        async with session.get(url=image_uri, proxy=CONFIG.PROXY) as response:
            if response.status == 200:
                image_bytes = await response.read()
                # Encode the bytes to a base64 string
                base64_string = base64.b64encode(image_bytes).decode("utf-8")
                return base64_string
            else:
                raise_provider_api_error(f"Failed to fetch image from {image_uri}")

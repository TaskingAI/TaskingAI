import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class BookSearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        earliest_year: int = plugin_input.input_params.get("earliest_year", None)
        latest_year: int = plugin_input.input_params.get("latest_year", None)
        isbn: str = plugin_input.input_params.get("isbn", None)
        number: int = plugin_input.input_params.get("number", None)
        min_rating: float = plugin_input.input_params.get("min_rating", None)
        max_rating: float = plugin_input.input_params.get("max_rating", None)

        bigbook_api = credentials.credentials.get("BIGBOOK_API_API_KEY")

        api_url = f"https://api.bigbookapi.com/search-books?api-key={bigbook_api}&query={query}"

        if earliest_year:
            api_url += f"&earliest-publish-year={earliest_year}"
        if latest_year:
            api_url += f"&latest-publish-year={latest_year}"
        if isbn:
            api_url += f"&isbn={isbn}"
        if number:
            if number < 1 or number > 100:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"Invalid number '{number}'. The number must be between 1 and 100.",
                )
            api_url += f"&number={number}"
        if min_rating:
            if min_rating < 0 or min_rating > 1:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"Invalid minimum rating '{min_rating}'. The minimum rating must be between 0 and 1.",
                )
            api_url += f"&min-rating={min_rating}"
        if max_rating:
            if max_rating < 0 or max_rating > 1:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"Invalid maximum rating '{max_rating}'. The maximum rating must be between 0 and 1.",
                )
            api_url += f"&max-rating={max_rating}"

        async with ClientSession() as session:
            async with session.get(url=api_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    books = data.get("books", [])
                    results = []
                    for book in books:
                        result = {}
                        id = book[0].get("id")
                        result["id"] = book[0].get("id")
                        result["title"] = book[0].get("title")
                        info_url = f"https://api.bigbookapi.com/{id}?api-key={bigbook_api}"
                        async with session.get(url=info_url, proxy=CONFIG.PROXY) as info_response:
                            if info_response.status == 200:
                                info_data = await info_response.json()
                                result["identifiers"] = info_data.get("identifiers")
                                result["authors"] = info_data.get("authors")
                                result["description"] = info_data.get("description")
                            else:
                                data = await info_response.json()
                                raise_provider_api_error(json.dumps(data))
                        results.append(result)

                    return PluginOutput(data={"results": json.dumps(results)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))

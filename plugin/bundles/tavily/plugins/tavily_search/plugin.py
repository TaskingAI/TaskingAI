import json
from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class TavilySearch(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        search_depth: str = plugin_input.input_params.get("search_depth", None)
        topic: str = plugin_input.input_params.get("topic", None)
        max_results: int = plugin_input.input_params.get("max_results", None)
        include_image: bool = plugin_input.input_params.get("include_image", None)
        include_answer: bool = plugin_input.input_params.get("include_answer", None)
        include_raw_content: bool = plugin_input.input_params.get("include_raw_content", None)
        use_cache: bool = plugin_input.input_params.get("use_cache", None)

        tavily_api_key: str = credentials.credentials.get("TAVILY_API_KEY")

        api_url = "https://api.tavily.com/search"

        body = {"api_key": tavily_api_key, "query": query}
        if search_depth:
            body["search_depth"] = search_depth
        if topic:
            body["topic"] = topic
        if max_results:
            body["max_results"] = max_results
        if include_image:
            body["include_image"] = include_image
        if include_answer:
            body["include_answer"] = include_answer
        if include_raw_content:
            body["include_raw_content"] = include_raw_content
        if use_cache:
            body["use_cache"] = use_cache

        headers = {"Content-Type": "application/json"}

        async with ClientSession() as session:
            async with session.post(url=api_url, json=body, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results")
                    optimized_results = []
                    for result in results:
                        optimized_results.append(
                            {
                                "title": result.get("title"),
                                "url": result.get("url"),
                                "content": result.get("content"),
                                "published_date": result.get("published_date"),
                            }
                        )
                    return PluginOutput(data={"result": json.dumps(optimized_results)})
                else:
                    data = await response.text()
                    return PluginOutput(data={"result": data})

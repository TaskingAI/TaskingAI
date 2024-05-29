from bundle_dependency import *
from duckduckgo_search import AsyncDDGS


class SearchImage(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        try:
            keywords: str = plugin_input.input_params.get("keywords")
            safe_search: str = "moderate"

            search_results = await AsyncDDGS().images(keywords=keywords, safesearch=safe_search)
            optimized_results = []
            for result in search_results:
                optimized_results.append(
                    {
                        "title": result.get("title", ""),
                        "web_url": result.get("url", ""),
                        "image_url": result.get("image", ""),
                        "height": result.get("height", ""),
                        "width": result.get("width", ""),
                    }
                )
            return PluginOutput(data={"results": optimized_results})
        except Exception as e:
            raise_provider_api_error(str(e))

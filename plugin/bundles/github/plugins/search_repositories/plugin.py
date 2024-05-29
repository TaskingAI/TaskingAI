import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class SearchRepositories(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        query: str = plugin_input.input_params.get("query")
        github_api_key: str = credentials.credentials.get("GITHUB_API_KEY")

        url = f"https://api.github.com/search/repositories?q={query}"

        headers = {
            "Authorization": f"Bearer {github_api_key}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data["items"]
                    useful_data = []
                    for item in items:
                        useful_data.append(
                            {
                                "name": item["name"],
                                "full_name": item["full_name"],
                                "description": item["description"],
                                "html_url": item["html_url"],
                                "stargazers_count": item["stargazers_count"],
                                "watchers_count": item["watchers_count"],
                                "forks_count": item["forks_count"],
                                "open_issues_count": item["open_issues_count"],
                                "language": item["language"],
                                "created_at": item["created_at"],
                                "updated_at": item["updated_at"],
                                "license": item["license"]["name"] if item["license"] else None,
                                "owner": {
                                    "login": item["owner"]["login"],
                                    "avatar_url": item["owner"]["avatar_url"],
                                    "html_url": item["owner"]["html_url"],
                                },
                            }
                        )
                    return PluginOutput(data={"result": json.dumps(useful_data)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))

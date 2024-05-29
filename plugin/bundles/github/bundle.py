from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class Github(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        query: str = "taskingai"
        github_api_key: str = credentials.credentials.get("GITHUB_API_KEY")

        url = f'https://api.github.com/search/repositories?q={query}'

        headers = {
            'Authorization': f'Bearer {github_api_key}',
            'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

        async with ClientSession() as session:
            async with session.get(url=url, headers=headers, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()

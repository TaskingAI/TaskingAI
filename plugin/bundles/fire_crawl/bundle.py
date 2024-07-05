from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class FireCrawl(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        FIRE_CRAWL_API_KEY: str = credentials.credentials.get("FIRE_CRAWL_API_KEY")
        url: str = "https://tasking.ai"
        only_main_content: bool = True
        screenshot: bool = True

        api_url = f"https://api.firecrawl.dev/v0/scrape"

        body = {"url": url, "pageOptions": {"onlyMainContent": only_main_content, "screenshot": screenshot}}

        headers = {"Authorization": f"Bearer {FIRE_CRAWL_API_KEY}", "Content-Type": "application/json"}

        async with ClientSession() as session:
            async with session.post(api_url, json=body, headers=headers, proxy=CONFIG.PROXY) as resp:
                if resp.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()

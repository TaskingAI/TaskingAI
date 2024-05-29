from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class NewsApi(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        country: str = "us"
        category: str = "business"
        count: int = 10

        news_api_key: str = credentials.credentials.get("NEWS_API_API_KEY")

        url = (
            f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={news_api_key}&pageSize={count}&page=1"
            + (f"&category={category}" if category else "")
        )

        if category is not None and category not in [
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology",
        ]:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid category")

        async with ClientSession() as session:
            async with session.get(url=url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()

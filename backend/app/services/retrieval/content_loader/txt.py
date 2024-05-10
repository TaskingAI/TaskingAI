from .base import BaseFileLoader
from langchain_community.document_loaders import TextLoader


class TxtContentLoader(BaseFileLoader):
    async def read_content(self, path):
        loader = TextLoader(path)
        data = loader.load()[0]
        return data.page_content

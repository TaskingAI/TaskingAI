from .base import BaseFileLoader

from langchain_community.document_loaders import UnstructuredHTMLLoader


class HtmlFileContentLoader(BaseFileLoader):
    async def read_content(self, path):
        html_loader = UnstructuredHTMLLoader(path)
        data = html_loader.load()

        result = [page.page_content for page in data]

        return "\n\n".join(result)

from .base import BaseFileLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader


class MarkdownFileContentLoader(BaseFileLoader):
    async def read_content(self, path):
        markdown_loader = UnstructuredMarkdownLoader(path)
        data = markdown_loader.load()

        result = [page.page_content for page in data]

        return "\n\n".join(result)

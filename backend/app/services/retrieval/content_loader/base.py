from abc import ABC, abstractmethod


class BaseFileLoader(ABC):
    @abstractmethod
    async def read_content(self, input_data):
        pass

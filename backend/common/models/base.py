from enum import Enum
from typing import List, Tuple

__all__ = ["SerializePurpose", "Status", "SortOrderEnum", "ListResult"]


class SerializePurpose(int, Enum):
    REDIS = 1
    RESPONSE = 2


class Status(int, Enum):
    CREATING = 0
    READY = 1
    DELETING = 2
    ERROR = 3
    PARTIAL = 4


class SortOrderEnum(str, Enum):
    desc = "desc"
    asc = "asc"


ListResult = Tuple[List, int, bool]

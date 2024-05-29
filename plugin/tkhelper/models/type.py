from enum import Enum
from typing import List, Tuple

__all__ = ["Status", "SortOrderEnum", "ListResult"]


class Status(str, Enum):
    CREATING = "creating"
    READY = "ready"
    DELETING = "deleting"
    ERROR = "error"
    PARTIAL = "partial"


class SortOrderEnum(str, Enum):
    DESC = "desc"
    ASC = "asc"


ListResult = Tuple[List, bool]

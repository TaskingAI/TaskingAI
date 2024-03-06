import logging
from enum import Enum


logger = logging.getLogger(__name__)

__all__ = [
    "ServiceType",
]


class ServiceType(str, Enum):
    GET = "get"
    LIST = "list"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RUN = "run"

# -*- coding: utf-8 -*-

# chunk_list_response.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Dict, List

__all__ = ["ChunkListResponse"]


class ChunkListResponse(BaseModel):
    status: str = Field("success")
    data: List[Dict] = Field(...)
    fetched_count: int = Field(...)
    has_more: bool = Field(...)

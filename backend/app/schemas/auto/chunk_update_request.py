# -*- coding: utf-8 -*-

# chunk_update_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict

__all__ = ["ChunkUpdateRequest"]


class ChunkUpdateRequest(BaseModel):
    content: Optional[str] = Field(None)
    metadata: Optional[Dict] = Field(None, min_length=0, max_length=16)

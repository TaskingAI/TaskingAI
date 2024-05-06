# -*- coding: utf-8 -*-

# chat_update_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict

__all__ = ["ChatUpdateRequest"]


class ChatUpdateRequest(BaseModel):
    metadata: Optional[Dict] = Field(None, min_length=0, max_length=16)
    name: Optional[str] = Field(None, min_length=0, max_length=127)

# -*- coding: utf-8 -*-

# chat_create_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Dict

__all__ = ["ChatCreateRequest"]


class ChatCreateRequest(BaseModel):
    metadata: Dict = Field({}, min_length=0, max_length=16)

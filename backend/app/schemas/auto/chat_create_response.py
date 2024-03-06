# -*- coding: utf-8 -*-

# chat_create_response.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Dict

__all__ = ["ChatCreateResponse"]


class ChatCreateResponse(BaseModel):
    status: str = Field("success")
    data: Dict = Field(...)

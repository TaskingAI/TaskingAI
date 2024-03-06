# -*- coding: utf-8 -*-

# message_create_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Dict
from app.models import *

__all__ = ["MessageCreateRequest"]


class MessageCreateRequest(BaseModel):
    role: MessageRole = Field(...)
    content: MessageContent = Field(...)
    metadata: Dict = Field({}, min_length=0, max_length=16)

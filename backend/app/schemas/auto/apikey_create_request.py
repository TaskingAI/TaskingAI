# -*- coding: utf-8 -*-

# apikey_create_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field

__all__ = ["ApikeyCreateRequest"]


class ApikeyCreateRequest(BaseModel):
    name: str = Field(...)

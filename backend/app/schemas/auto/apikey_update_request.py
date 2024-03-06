# -*- coding: utf-8 -*-

# apikey_update_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Optional

__all__ = ["ApikeyUpdateRequest"]


class ApikeyUpdateRequest(BaseModel):
    name: Optional[str] = Field(None)

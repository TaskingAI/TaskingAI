# -*- coding: utf-8 -*-

# action_update_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from app.models import *

__all__ = ["ActionUpdateRequest"]


class ActionUpdateRequest(BaseModel):
    openapi_schema: Optional[Dict] = Field(None)
    authentication: Optional[ActionAuthentication] = Field(None)

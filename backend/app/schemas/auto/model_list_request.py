# -*- coding: utf-8 -*-

# model_list_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.models import *

__all__ = ["ModelListRequest"]


class ModelListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100)
    order: Optional[SortOrderEnum] = Field(SortOrderEnum.DESC)
    after: Optional[str] = Field(None, min_length=1, max_length=50)
    before: Optional[str] = Field(None, min_length=1, max_length=50)
    equal_filter: Optional[str] = Field(None)
    prefix_filter: Optional[str] = Field(None)

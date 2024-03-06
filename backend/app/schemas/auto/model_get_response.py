# -*- coding: utf-8 -*-

# model_get_response.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Dict

__all__ = ["ModelGetResponse"]


class ModelGetResponse(BaseModel):
    status: str = Field("success")
    data: Dict = Field(...)

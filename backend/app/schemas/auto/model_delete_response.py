# -*- coding: utf-8 -*-

# model_delete_response.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field

__all__ = ["ModelDeleteResponse"]


class ModelDeleteResponse(BaseModel):
    status: str = Field("success")

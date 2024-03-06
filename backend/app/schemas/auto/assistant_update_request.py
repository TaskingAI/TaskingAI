# -*- coding: utf-8 -*-

# assistant_update_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from app.models import *

__all__ = ["AssistantUpdateRequest"]


class AssistantUpdateRequest(BaseModel):
    model_id: Optional[str] = Field(None, min_length=8, max_length=8, pattern="^[a-zA-Z0-9]+$")
    name: Optional[str] = Field(None, min_length=0, max_length=127)
    description: Optional[str] = Field(None, min_length=0, max_length=512)
    system_prompt_template: Optional[List[str]] = Field(None)
    memory: Optional[AssistantMemory] = Field(None)
    tools: Optional[List[ToolRef]] = Field(None)
    retrievals: Optional[List[RetrievalRef]] = Field(None)
    retrieval_configs: Optional[RetrievalConfig] = Field(None)
    metadata: Optional[Dict] = Field(None, min_length=0, max_length=16)

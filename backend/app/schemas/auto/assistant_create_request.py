# -*- coding: utf-8 -*-

# assistant_create_request.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from pydantic import BaseModel, Field
from typing import Dict, List
from app.models import *

__all__ = ["AssistantCreateRequest"]


class AssistantCreateRequest(BaseModel):
    model_id: str = Field(..., min_length=8, max_length=8, pattern="^[a-zA-Z0-9]+$")
    name: str = Field("", min_length=0, max_length=127)
    description: str = Field("", min_length=0, max_length=512)
    system_prompt_template: List[str] = Field([])
    memory: AssistantMemory = Field(...)
    tools: List[ToolRef] = Field([])
    retrievals: List[RetrievalRef] = Field([])
    retrieval_configs: RetrievalConfig = Field(...)
    metadata: Dict = Field({}, min_length=0, max_length=16)

from pydantic import BaseModel, Field
from typing import List


class AssistantTool(BaseModel):
    type: str = Field(..., pattern="function|action", description="The tool type, which can be `function` or `action`.")
    id: str = Field(..., description="The tool ID.")


# GET /projects/{project_id}/fetch_tools


class ToolFetchRequest(BaseModel):
    tools: List[AssistantTool] = Field(..., description="A list of tools.")
    # error_if_not_found: bool = Field(default=False, description="If true, an error will be raised if any tool is not found.")

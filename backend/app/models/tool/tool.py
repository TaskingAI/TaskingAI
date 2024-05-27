from pydantic import BaseModel, Field
from typing import Dict, Union, List
from enum import Enum
import json

__all__ = ["ToolType", "ToolRef", "Tool", "ToolInput", "ToolOutput"]


class ToolType(str, Enum):
    ACTION = "action"
    PLUGIN = "plugin"


class ToolRef(BaseModel):
    type: ToolType = Field(..., description="The tool type.")
    id: str = Field(..., description="The tool ID.")


class Tool(BaseModel):
    tool_id: str = Field(
        ...,
        description="The tool ID.",
        examples=["action_1"],
    )

    type: ToolType = Field(
        ...,
        description="The tool type, which can be `action`, `plugin` or `function`.",
        examples=["action", "plugin", "function"],
    )

    function_def: Dict = Field(
        ...,
        description="The function definition for chat completion function-call.",
    )

    def function_name(self):
        return self.function_def["name"]


class ToolInput(BaseModel):
    type: ToolType = Field(
        ...,
        description="The tool type, which can be `function` or `action`.",
        examples=["action", "plugin"],
    )

    tool_id: str = Field(
        ...,
        description="The tool ID.",
        examples=["action_1"],
    )

    tool_call_id: str = Field(
        ...,
        description="The tool call ID.",
        examples=["call_1"],
    )

    arguments: Dict = Field(
        ...,
        description="The tool input arguments.",
    )


class ToolOutput(BaseModel):
    type: ToolType = Field(
        ...,
        description="The tool type, which can be `function` or `action`.",
        examples=["action", "plugin"],
    )

    tool_id: str = Field(
        ...,
        description="The tool ID.",
        examples=["action_1"],
    )

    tool_call_id: str = Field(
        ...,
        description="The tool call ID.",
        examples=["call_1"],
    )

    status: int = Field(
        ...,
        description="The tool output status.",
        examples=[200, 400, 500],
    )

    data: Union[Dict, List] = Field(
        ...,
        description="The tool output data.",
    )

    def to_function_message(self):
        if self.status == 200:
            return {
                "role": "function",
                "content": json.dumps(self.data),
                "id": self.tool_call_id,
            }
        else:
            return {
                "role": "function",
                "content": json.dumps({"status": self.status, "error": self.data}),
                "id": self.tool_call_id,
            }

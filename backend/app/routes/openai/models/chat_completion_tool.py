from pydantic import BaseModel, Field
from .chat_completion_function import OpenaiFunctionCall, OpenaiFunction
from typing import Literal


class OpenaiTool(BaseModel):
    function: OpenaiFunction = Field(..., description="Required[FunctionDefinition]")

    type: Literal["function"] = Field(..., description="The type of the tool. Currently, only function is supported.")


class OpenaiChatCompletionMessageToolCallParam(BaseModel):
    id: str = Field(..., description="The ID of the tool call.")

    function: OpenaiFunctionCall = Field(..., description="The function that the model called.")

    type: Literal["function"] = Field(..., description="The type of the tool. Currently, only function is supported.")

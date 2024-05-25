from typing import Dict, List
from tkhelper.utils import current_timestamp_int_milliseconds

from app.models import MessageGenerationLog, Model, RetrievalResult, ToolInput, ToolOutput

__all__ = [
    "build_retrieval_input_log_dict",
    "build_retrieval_output_log_dict",
    "build_tool_input_log_dict",
    "build_tool_output_log_dict",
    "build_chat_completion_input_log_dict",
    "build_chat_completion_output_log_dict",
]


def build_retrieval_input_log_dict(
    session_id: str,
    event_id: str,
    query_text: str,
    top_k: int,
):
    return MessageGenerationLog(
        session_id=session_id,
        event="retrieval",
        event_id=event_id,
        event_step="input",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "query_text": query_text,
            "top_k": top_k,
        },
    ).model_dump()


def build_retrieval_output_log_dict(
    session_id: str,
    event_id: str,
    retrieval_result: List[RetrievalResult],
):
    return MessageGenerationLog(
        session_id=session_id,
        event="retrieval",
        event_id=event_id,
        event_step="output",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "result": retrieval_result,
        },
    ).model_dump()


def build_tool_input_log_dict(
    session_id: str,
    event_id: str,
    tool_input: ToolInput,
):
    return MessageGenerationLog(
        session_id=session_id,
        event="tool",
        event_id=event_id,
        event_step="input",
        timestamp=current_timestamp_int_milliseconds(),
        content=tool_input.model_dump(),
    ).model_dump()


def build_tool_output_log_dict(
    session_id: str,
    event_id: str,
    # tool_name: str,
    tool_output: ToolOutput,
):
    return MessageGenerationLog(
        session_id=session_id,
        event="tool",
        event_id=event_id,
        event_step="output",
        timestamp=current_timestamp_int_milliseconds(),
        content=tool_output.model_dump(),
    ).model_dump()


def build_chat_completion_input_log_dict(
    session_id: str,
    event_id: str,
    model: Model,
    messages: List[Dict],
    functions: List[Dict],
):
    log = MessageGenerationLog(
        session_id=session_id,
        event="chat_completion",
        event_id=event_id,
        event_step="input",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "model_id": model.model_id,
            "model_schema_id": model.model_schema_id,
            "provider_model_id": model.provider_model_id,
            "messages": messages,
            "functions": functions,
        },
    )
    return log.model_dump()


def build_chat_completion_output_log_dict(
    session_id: str,
    event_id: str,
    model: Model,
    message: Dict,
    usage: Dict,
):
    return MessageGenerationLog(
        session_id=session_id,
        event="chat_completion",
        event_id=event_id,
        event_step="output",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "model_id": model.model_id,
            "model_schema_id": model.model_schema_id,
            "provider_model_id": model.provider_model_id,
            "message": message,
            "usage": usage,
        },
    ).model_dump()

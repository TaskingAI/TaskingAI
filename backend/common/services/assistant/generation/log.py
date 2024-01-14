from common.models import MessageGenerationLog, Chunk
from typing import Dict, List
from common.utils import current_timestamp_int_milliseconds


def build_retrieval_collection_input_log_dict(
    session_id: str,
    event_id: str,
    collection_ids: List[str],
    query_text: str,
    top_k: int,
):
    return MessageGenerationLog(
        session_id=session_id,
        event="retrieval",
        event_id=event_id,
        event_step="retrieval_input",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "collection_ids": collection_ids,
            "arguments": {
                "query_text": query_text,
                "top_k": top_k,
            },
        },
    ).model_dump()


def build_retrieval_collection_output_log_dict(
    session_id: str,
    event_id: str,
    collection_ids: List[str],
    chunks: List[Chunk],
):
    return MessageGenerationLog(
        session_id=session_id,
        event="retrieval",
        event_id=event_id,
        event_step="retrieval_output",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "collection_ids": collection_ids,
            "result": {"chunks": [chunk.model_dump() for chunk in chunks]},
        },
    ).model_dump()


def build_tool_action_input_log_dict(session_id: str, event_id: str, action_id: str, name: str, arguments: Dict):
    return MessageGenerationLog(
        session_id=session_id,
        event="tool",
        event_id=event_id,
        event_step="action_input",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "action_id": action_id,
            "name": name,
            "arguments": arguments,
        },
    ).model_dump()


def build_tool_action_output_log_dict(session_id: str, event_id: str, action_id: str, name: str, output: Dict):
    return MessageGenerationLog(
        session_id=session_id,
        event="tool",
        event_id=event_id,
        event_step="action_output",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "action_id": action_id,
            "name": name,
            "result": output,
        },
    ).model_dump()


def build_chat_completion_input_log_dict(
    session_id: str,
    event_id: str,
    provider_model_id: str,
    messages: List[Dict],
    functions: List[Dict],
):
    log = MessageGenerationLog(
        session_id=session_id,
        event="chat_completion",
        event_id=event_id,
        event_step="chat_completion_input",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "provider_model_id": provider_model_id,
            "messages": messages,
            "functions": functions,
        },
    )
    return log.model_dump()


def build_chat_completion_output_log_dict(
    session_id: str,
    event_id: str,
    provider_model_id: str,
    message: Dict,
):
    return MessageGenerationLog(
        session_id=session_id,
        event="chat_completion",
        event_id=event_id,
        event_step="chat_completion_output",
        timestamp=current_timestamp_int_milliseconds(),
        content={
            "provider_model_id": provider_model_id,
            "message": message,
        },
    ).model_dump()

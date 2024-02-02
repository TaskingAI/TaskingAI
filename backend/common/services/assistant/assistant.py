from typing import Optional, Dict, List
from common.models import (
    Assistant,
    SortOrderEnum,
    ListResult,
    AssistantTool,
    AssistantRetrieval,
    AssistantRetrievalConfig,
    AssistantRetrievalMethod,
    Model,
    ModelType,
    AssistantMemory,
)
from common.database_ops.assistant import assistant as db_assistant
from common.error import ErrorCode, raise_http_error
from common.services.tool.action import get_action
from common.services.retrieval.collection import get_collection
from common.services.model.model import get_model

__all__ = [
    "list_assistants",
    "create_assistant",
    "update_assistant",
    "get_assistant",
    "delete_assistant",
]


async def validate_and_get_assistant(assistant_id: str) -> Assistant:
    assistant = await db_assistant.get_assistant(assistant_id)
    if not assistant:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Assistant {assistant_id} not found.")
    return assistant


async def list_assistants(
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    id_search: Optional[str],
    name_search: Optional[str],
) -> ListResult:
    """
    List assistants
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :param offset: the offset of the query
    :param id_search: the assistant ID to search for
    :param name_search: the assistant name to search for
    :return: a list of assistants, total count of assistants, and whether there are more assistants
    """

    after_assistant, before_assistant = None, None

    if after:
        after_assistant = await validate_and_get_assistant(after)

    if before:
        before_assistant = await validate_and_get_assistant(before)

    return await db_assistant.list_assistants(
        limit=limit,
        order=order,
        after_assistant=after_assistant,
        before_assistant=before_assistant,
        offset=offset,
        prefix_filters={
            "assistant_id": id_search,
            "name": name_search,
        },
    )


async def _validate_tools(
    tools: List[AssistantTool],
    model_function_call_enabled: bool,
    model_id: str,
):
    """
    Validate tools
    :param tools: a list of assistant tools
    :param model_function_call_enabled: if the model supports function call
    :param model_id: assistant model id
    :return:
    """

    if not model_function_call_enabled:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"The assistant's language model {model_id} does not support function call to use the tools.",
        )

    for tool in tools:
        if tool.type == "action":
            await get_action(tool.id)
        # todo: support more tool types
        else:
            raise NotImplementedError(f"Tool type {tool.type} is not supported yet.")


async def _validate_retrievals(
    retrievals: List[AssistantRetrieval],
    retrieval_configs: AssistantRetrievalConfig,
    model_function_call_enabled: bool,
    model_id: str,
):
    """
    Validate retrievals
    :param retrievals: a list of assistant retrievals
    :param retrieval_configs: assistant retrieval configs
    :param model_function_call_enabled: if the model supports function call
    :param model_id: assistant model id
    :return:
    """

    if retrieval_configs.method == AssistantRetrievalMethod.FUNCTION_CALL and not model_function_call_enabled:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"The assistant's language model {model_id} does not support function call to use retrieval.",
        )

    for retrieval in retrievals:
        if retrieval.type == "collection":
            await get_collection(retrieval.id)
        else:
            raise NotImplementedError(f"Retrieval type {retrieval.type} is not supported yet.")


async def create_assistant(
    model_id: str,
    name: str,
    description: str,
    system_prompt_template: List[str],
    memory: AssistantMemory,
    tools: List,
    # tool_configs: Dict,
    retrievals: List,
    retrieval_configs: AssistantRetrievalConfig,
    metadata: Dict,
) -> Assistant:
    """
    Create assistant
    :param model_id: model id
    :param name: assistant name
    :param description: assistant description
    :param system_prompt_template: system prompt template
    :param memory: the assistant memory
    :param tools: the assistant tools, a list of tuple (type, id)
    # :param tool_configs: the assistant tool configs
    :param retrievals: the assistant retrievals, a list of tuple (type, id)
    :param retrieval_configs: the assistant retrieval configs
    :param metadata: the assistant metadata
    :return: the created assistant
    """

    # validate chat completion model
    model: Model = await get_model(model_id)
    if not model.type == ModelType.CHAT_COMPLETION:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Model {model_id} is not a valid chat completion model.",
        )
    model_function_call_enabled = model.properties.get("function_call", False)

    # validate tools
    if tools:
        await _validate_tools(
            tools=tools,
            model_function_call_enabled=model_function_call_enabled,
            model_id=model_id,
        )

    # validate retrievals
    if retrievals:
        await _validate_retrievals(
            retrievals=retrievals,
            retrieval_configs=retrieval_configs,
            model_function_call_enabled=model_function_call_enabled,
            model_id=model_id,
        )

    # create assistant
    assistant = await db_assistant.create_assistant(
        name=name,
        description=description,
        model_id=model_id,
        system_prompt_template=system_prompt_template,
        memory=memory.model_dump(),
        tools=[t.model_dump() for t in tools],
        tool_configs={},
        retrievals=[r.model_dump() for r in retrievals],
        retrieval_configs=retrieval_configs.model_dump(),
        metadata=metadata,
    )
    return assistant


async def update_assistant(
    assistant_id: str,
    model_id: Optional[str],
    name: Optional[str],
    description: Optional[str],
    system_prompt_template: Optional[List[str]],
    memory: Optional[AssistantMemory],
    tools: Optional[List],
    # tool_configs: Optional[Dict],
    retrievals: Optional[List],
    retrieval_configs: Optional[AssistantRetrievalConfig],
    metadata: Optional[Dict],
) -> Assistant:
    """
    Update assistant
    :param assistant_id: the assistant id
    :param model_id: model id
    :param name: assistant name
    :param description: assistant description
    :param system_prompt_template: system prompt template
    :param memory: the assistant memory
    :param tools: the assistant tools, a list of tuple (type, id)
    # :param tool_configs: the assistant tool configs
    :param retrievals: the assistant retrievals, a list of tuple (type, id)
    :param retrieval_configs: the assistant retrieval configs
    :param metadata: the assistant metadata
    :return: the updated assistant
    """

    # get assistant
    assistant: Assistant = await validate_and_get_assistant(assistant_id=assistant_id)

    # prepare update dict
    update_dict = {}

    if model_id is not None:
        update_dict["model_id"] = model_id
    else:
        model_id = assistant.model_id

    if name is not None:
        update_dict["name"] = name

    if description is not None:
        update_dict["description"] = description

    if system_prompt_template is not None:
        update_dict["system_prompt_template"] = system_prompt_template

    if memory is not None:
        update_dict["memory"] = memory.model_dump()

    if tools is not None:
        update_dict["tools"] = [t.model_dump() for t in tools]
    else:
        tools = assistant.tools

    if retrievals is not None:
        update_dict["retrievals"] = [r.model_dump() for r in retrievals]
    else:
        retrievals = assistant.retrievals

    if retrieval_configs is not None:
        update_dict["retrieval_configs"] = retrieval_configs.model_dump()
    else:
        retrieval_configs = assistant.retrieval_configs

    # get model properties
    model: Model = await get_model(model_id)
    model_function_call_enabled = model.properties.get("function_call", False)

    # validate tools
    if tools:
        await _validate_tools(
            tools=tools,
            model_function_call_enabled=model_function_call_enabled,
            model_id=model_id,
        )

    # validate retrievals
    if retrievals:
        await _validate_retrievals(
            retrievals=retrievals,
            retrieval_configs=retrieval_configs,
            model_function_call_enabled=model_function_call_enabled,
            model_id=model_id,
        )

    if name:
        update_dict["name"] = name
    if description:
        update_dict["description"] = description
    if metadata:
        update_dict["metadata"] = metadata

    if update_dict:
        assistant = await db_assistant.update_assistant(
            assistant=assistant,
            update_dict=update_dict,
        )

    return assistant


async def get_assistant(assistant_id: str) -> Assistant:
    """
    Get assistant
    :param assistant_id: the assistant id
    :return: the assistant
    """

    assistant: Assistant = await validate_and_get_assistant(assistant_id)
    return assistant


async def delete_assistant(assistant_id: str) -> None:
    """
    Delete assistant
    :param assistant_id: the assistant id
    """

    assistant: Assistant = await validate_and_get_assistant(assistant_id)
    await db_assistant.delete_assistant(assistant)

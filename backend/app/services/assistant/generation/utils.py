import re
from typing import Dict, List, Optional, Tuple
from tkhelper.utils import generate_random_id

from app.models import Assistant, RetrievalMethod, Chat, RetrievalResult
from app.services.retrieval.retrieval import query_retrievals


class MessageGenerationException(Exception):
    pass


def build_system_prompt(
    system_prompt_template: List[str],
    system_prompt_variables: Dict,
    # context_summary: Optional[str],
    retrieval_doc: Optional[str],
) -> str:
    """
    Generates a system prompt by substituting variables in a template with provided values.

    :param system_prompt_template: A list of template strings with placeholders for variables.
    :param system_prompt_variables: A dictionary mapping variable names to their values.
    :param retrieval_doc: A related document to be appended to the prompt.
    :return: The final prompt string with variable substitutions made and optional context and document appended.

    Note:
    - Placeholders in the templates are expected to be in the format `{{variable_name}}`.
    - A template is skipped if it contains a placeholder for which there is no corresponding variable
      in the `system_prompt_variables`, or if the variable's value is `None` or another illegal value.
    - The `context_summary` and `retrieval_doc` are appended to the end of the prompt if provided.
    """

    # Initialize an empty list to collect the finalized prompt segments.
    final_prompt_list = []

    # Replace all the variable placeholders in the template with their values.
    for prompt in system_prompt_template:
        var_names = re.findall(r"{{(.*?)}}", prompt)
        for var in var_names:
            if var in system_prompt_variables and system_prompt_variables[var] is not None:
                prompt = prompt.replace("{{" + var + "}}", str(system_prompt_variables[var]))
            else:
                break
        else:
            final_prompt_list.append(prompt)

    final_prompt = "\n\n".join(final_prompt_list)

    # If a related document is provided, append it to the final prompt with a separator.
    if retrieval_doc:
        final_prompt += f"\n\n-------\nRELATED DOCUMENT: {retrieval_doc}"

    # If a context summary is provided, append it to the final prompt with a separator.
    # if context_summary:
    #     final_prompt += f"\n\n-------\nCONVERSATION CONTEXT SUMMARY: {context_summary}"

    # Return the final prompt string.
    return final_prompt


def build_chat_completion_messages(system_prompt: str, history_messages: List[Dict]) -> List[Dict]:
    """
    Prepares a list of chat messages for completion, starting with a system prompt followed by historical messages.

    :param system_prompt: A string that contains the system's current prompt or message to the user.
    :param history_messages: A list of dictionaries, each representing a prior message in the chat history.
    :return: A list of chat messages starting with the system's prompt followed by the history messages.
    """
    return [{"role": "system", "content": system_prompt}] + history_messages


async def get_chat_memory_messages(chat: Chat):
    """
    Retrieves and validates the chat memory from a given chat.

    :param chat: A Chat object.
    :return: A tuple containing chat memory messages and context summary.
    :raises: An HTTP error if validation fails.
    """

    # Extract messages and context summary from the chat memory
    chat_memory_messages = chat.memory.messages

    # Validate the chat memory to ensure it ends with a user message
    if chat_memory_messages:
        last_message = chat_memory_messages[-1]
        if last_message.role == "assistant":
            raise MessageGenerationException("Cannot generate another assistant message after an assistant message.")

    # Ensure there is at least one user message in the chat memory
    user_message_count = sum(1 for message in chat_memory_messages if message.role == "user")
    if user_message_count == 0:
        raise MessageGenerationException("There is no user message in the chat context.")

    message_dicts = [message.model_dump() for message in chat_memory_messages]
    return message_dicts


async def query_assistant_retrieval(
    assistant: Assistant,
    query_text: str,
) -> Tuple[str, List[RetrievalResult]]:
    """
     Retrieve related documents.
    :param assistant: assistant object
    :param query_text: The query text to search within the collections.
    :return: A tuple containing the concatenated retrieval documents and the list of chunk objects.
    """

    # Perform the query to retrieve results
    results: List[RetrievalResult] = await query_retrievals(
        retrieval_refs=assistant.retrievals,
        top_k=assistant.retrieval_configs.top_k,
        max_tokens=assistant.retrieval_configs.max_tokens,
        score_threshold=assistant.retrieval_configs.score_threshold,
        query_text=query_text,
    )

    # Concatenate the text from each chunk into a single retrieval document
    retrieval_doc = "\n\n".join([result.content for result in results])

    return retrieval_doc, results


def build_retrieval_function_dict(existing_tool_names: List[str], description: str = None) -> Dict:
    """
    Constructs a unique retrieval function dictionary with a dynamic name to avoid conflicts.

    :param existing_tool_names: A list of names to ensure the new function has a unique name.
    :param description: An optional description for the retrieval function; defaults to a preset description.
    :return: A dictionary representing the retrieval function with its name, description, and parameter schema.
    """

    # Create a base function name and modify it if it conflicts with existing names
    base_name = name = "retrieve_related_docs"
    i = 0
    while name in existing_tool_names:
        i += 1
        name = f"{base_name}_{i}"

    # Use a default description if none is provided
    if not description:
        description = (
            "Retrieve a list of relevant documents when additional background knowledge "
            "or detailed information is required, based on the provided query text."
        )

    # Build and return the function dictionary
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {
                "query_text": {
                    "type": "string",
                    "description": "Text query for semantic search to find documents closely related to the topic, "
                    "focusing on contextual relevance.",
                }
            },
            "required": ["query_text"],
        },
    }


def get_system_prompt_retrieval_query_text(chat_memory_messages: List[Dict], method: RetrievalMethod):
    """
    Generates retrieval query text based on the specified retrieval method using chat memory messages.

    :param chat_memory_messages: A list of chat memory message dictionaries.
    :param method: The method by which to retrieve the query text, using an RetrievalMethod enum.
    :return: A string of the retrieval query text or None if not applicable.
    """

    retrieval_query_text = None

    # If MEMORY method is chosen, concatenate all chat memory messages
    if method == RetrievalMethod.MEMORY:
        retrieval_query_text = "\n\n".join([message["content"] or "" for message in chat_memory_messages])

    # If USER_MESSAGE method is chosen, concatenate latest user messages up to a system message
    elif method == RetrievalMethod.USER_MESSAGE:
        user_messages = []
        for message in reversed(chat_memory_messages):
            if message["role"] == "user":
                user_messages.append(message)
            else:
                break
        retrieval_query_text = "\n\n".join([message["content"] or "" for message in reversed(user_messages)])

    return retrieval_query_text


def generate_random_event_id():
    return "E5dK" + generate_random_id(20)


def generate_random_session_id():
    return "D9Js" + generate_random_id(20)

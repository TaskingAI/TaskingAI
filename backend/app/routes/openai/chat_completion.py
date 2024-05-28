from fastapi import APIRouter, Depends, Request

from app.operators import model_ops, assistant_ops
from app.services.inference.chat_completion import chat_completion, stream_chat_completion
from app.services.assistant.generation import StatelessNormalSession, StatelessStreamSession
from .utils import *
from starlette.responses import StreamingResponse
from app.models import Assistant
from tkhelper.utils import SSE_DONE_MSG


from ..utils import auth_info_required, is_model_id, is_assistant_id

router = APIRouter()


# add new add_api_key
@router.post(
    "/chat/completions",
    summary="Chat Completion",
    operation_id="chat_completion",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Model inference for chat completion.",
)
async def api_chat_completion_openai(
    request: Request,
    openai_data: OpenaiChatCompletionRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    data: ChatCompletionRequest = adapt_openai_chat_completion_input(openai_data)
    if is_model_id(model_id=data.model_id):
        # validate model
        model = await model_ops.get(model_id=data.model_id)
        # check function call ability
        functions = [function.model_dump() for function in data.functions] if data.functions is not None else None
        if functions and not model.allow_function_call():
            raise_request_validation_error(f"Model {model.model_id} does not support function calls.")

        # prepare messages
        messages = [message.model_dump() for message in data.messages]
        payload_dict = data.model_dump()

        # perform chat completion with model
        if data.stream:
            if not model.allow_streaming():
                raise_request_validation_error(f"Model {model.model_id} does not support streaming.")

            async def generator():
                chunk_id = generate_random_chat_completion_id()
                async for chunk_dict in await stream_chat_completion(
                    model=model,
                    messages=messages,
                    configs=data.configs,
                    function_call=data.function_call,
                    functions=functions,
                ):
                    openai_chunk = await to_openai_chunk(chunk_dict, chunk_id, openai_data)
                    if openai_chunk is not None:
                        yield f"data: {json.dumps(openai_chunk)}\n\n"
                yield SSE_DONE_MSG

            return StreamingResponse(
                generator(),
                media_type="text/event-stream",
            )

        else:
            # generate none stream response
            response_data = await chat_completion(
                model=model,
                messages=messages,
                configs=data.configs,
                function_call=data.function_call,
                functions=functions,
            )
            response = ChatCompletion(**response_data)
            openai_response = adapt_openai_chat_completion_response(response, openai_data)
            openai_response_dict = openai_response.model_dump()
            for choice in openai_response_dict["choices"] if openai_response_dict.get("choices") else []:
                message_dict = choice.get("message") or {}
                if message_dict["function_call"] is None:
                    del message_dict["function_call"]
                if message_dict["tool_calls"] is None:
                    del message_dict["tool_calls"]
                if message_dict["name"] is None:
                    del message_dict["name"]
            return openai_response_dict

    elif is_assistant_id(assistant_id=data.model_id):
        # validate assistant
        assistant: Assistant = await assistant_ops.get(assistant_id=data.model_id)

        # perform chat completion with assistant
        if data.stream:
            session = StatelessStreamSession(
                assistant=assistant,
                save_logs=False,  # todo: enable save_logs
                yield_dict=True,
            )

            async def generator():
                chunk_id = generate_random_chat_completion_id()
                async for chunk_dict in session.stream_generate(data.messages, data.functions):
                    openai_chunk = await to_openai_chunk(chunk_dict, chunk_id, openai_data)
                    if openai_chunk is not None:
                        yield f"data: {json.dumps(openai_chunk)}\n\n"
                yield SSE_DONE_MSG

            return StreamingResponse(
                generator(),
                media_type="text/event-stream",
            )
        else:
            session = StatelessNormalSession(
                assistant=assistant,
                save_logs=False,  # todo: enable save_logs
            )
            response = await session.generate(data.messages, data.functions)
            openai_response = adapt_openai_chat_completion_response(response.data, openai_data)
            openai_response_dict = openai_response.model_dump()
            for choice in openai_response_dict["choices"] if openai_response_dict.get("choices") else []:
                message_dict = choice.get("message") or {}
                if message_dict["function_call"] is None:
                    del message_dict["function_call"]
                if message_dict["tool_calls"] is None:
                    del message_dict["tool_calls"]
                if message_dict["name"] is None:
                    del message_dict["name"]
            return openai_response_dict

    else:
        raise_request_validation_error(f"Invalid model_id: {data.model_id}")

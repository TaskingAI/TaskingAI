from typing import Dict, List

from tkhelper.models import RedisOperator, ModelEntity
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.error import raise_request_validation_error

from app.database import redis_conn, postgres_pool
from app.models import Assistant, Model, ToolRef, RetrievalRef, RetrievalConfig, RetrievalMethod
from app.schemas import AssistantCreateRequest, AssistantUpdateRequest

from ..model import model_ops

__all__ = ["assistant_ops"]


async def _validate_tools(
    tools: List[ToolRef],
    model: Model,
):
    """
    Validate tools
    :param tools: a list of assistant tools
    :param model: the assistant model
    :return:
    """
    from app.services.tool import verify_tools

    if not tools:
        return

    if not model.allow_function_call():
        raise_request_validation_error(
            f"The assistant's language model {model.model_id} does not support function call to use the tools.",
        )

    await verify_tools(tools)


async def _validate_retrievals(
    retrievals: List[RetrievalRef],
    retrieval_configs: RetrievalConfig,
    model: Model,
):
    """
    Validate retrievals
    :param retrievals: a list of assistant retrievals
    :param retrieval_configs: assistant retrieval configs
    :param model: the assistant model
    :return:
    """
    from app.services.retrieval import verify_retrievals

    if not retrievals:
        return

    if retrieval_configs.method == RetrievalMethod.FUNCTION_CALL and not model.allow_function_call():
        raise_request_validation_error(
            f"The assistant's language model {model.model_id} does not support function call to use retrieval.",
        )

    await verify_retrievals(retrievals)


class AssistantModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        """
        Create an assistant
        :param create_dict: the assistant create dictionary
        :param kwargs: other parameters
        :return: the created assistant
        """

        self._check_kwargs(object_id_required=False, **kwargs)

        request = AssistantCreateRequest(**create_dict)
        model_id = request.model_id
        name = request.name
        description = request.description
        system_prompt_template = request.system_prompt_template
        memory = request.memory
        tools = request.tools
        retrievals = request.retrievals
        retrieval_configs = request.retrieval_configs
        metadata = request.metadata

        # validate model
        model: Model = await model_ops.get(model_id=model_id)
        if not model.is_chat_completion():
            raise_request_validation_error(
                f"Model {model_id} is not a valid chat completion model.",
            )

        # validate tools
        await _validate_tools(
            tools=tools,
            model=model,
        )

        # validate retrievals
        await _validate_retrievals(
            retrievals=retrievals,
            retrieval_configs=retrieval_configs,
            model=model,
        )

        assistant = await super().create(
            create_dict={
                "name": name,
                "description": description,
                "model_id": model_id,
                "system_prompt_template": system_prompt_template,
                "memory": memory.model_dump(),
                "tools": [t.model_dump() for t in tools],
                "tool_configs": {},
                "retrievals": [r.model_dump() for r in retrievals],
                "retrieval_configs": retrieval_configs.model_dump(),
                "metadata": metadata,
            },
        )
        return assistant

    async def update(
        self,
        update_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        """
        Update an assistant
        :param update_dict: the assistant update dictionary
        :param kwargs: other parameters
        :return: the updated assistant
        """

        self._check_kwargs(object_id_required=True, **kwargs)
        assistant_id = kwargs.get("assistant_id")

        request = AssistantUpdateRequest(**update_dict)
        model_id = request.model_id
        name = request.name
        description = request.description
        system_prompt_template = request.system_prompt_template
        memory = request.memory
        tools = request.tools
        retrievals = request.retrievals
        retrieval_configs = request.retrieval_configs
        metadata = request.metadata

        # get assistant
        assistant = await self.get(assistant_id=assistant_id)

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
        model: Model = await model_ops.get(model_id=model_id)

        # validate tools
        if tools:
            await _validate_tools(
                tools=tools,
                model=model,
            )

        # validate retrievals
        if retrievals:
            await _validate_retrievals(
                retrievals=retrievals,
                retrieval_configs=retrieval_configs,
                model=model,
            )

        if name:
            update_dict["name"] = name
        if description:
            update_dict["description"] = description
        if metadata:
            update_dict["metadata"] = metadata

        if update_dict:
            assistant = await super().update(
                update_dict=update_dict,
                **kwargs,
            )

        return assistant


assistant_ops = AssistantModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Assistant,
    redis=RedisOperator(
        entity_class=Assistant,
        redis_conn=redis_conn,
    ),
)

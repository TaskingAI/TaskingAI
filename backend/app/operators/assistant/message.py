from typing import Dict

from tkhelper.models import ModelEntity
from tkhelper.models.operator.postgres_operator import PostgresModelOperator

from app.database import postgres_pool
from app.models import Message, MessageContent, MessageRole, default_tokenizer, ChatMemory
from app.schemas import MessageCreateRequest

from .chat import chat_ops

__all__ = ["message_ops"]


class MessageModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        from app.services.assistant.chat import update_chat_memory

        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        assistant_id = kwargs.get("assistant_id")
        chat_id = kwargs.get("chat_id")

        # attributes
        request = MessageCreateRequest(**create_dict)
        role: MessageRole = request.role
        content: MessageContent = request.content
        metadata: Dict[str, str] = request.metadata

        # get chat
        chat = await chat_ops.get(
            assistant_id=assistant_id,
            chat_id=chat_id,
        )

        # count tokens
        # todo: enable other tokenizer
        num_tokens = default_tokenizer.count_tokens(content.text)

        # create message
        message = await super().create(
            assistant_id=assistant_id,
            chat_id=chat_id,
            create_dict={
                "role": role.value,
                "content": content.model_dump(),
                "num_tokens": num_tokens,
                "metadata": metadata,
            },
        )

        # update chat memory
        updated_chat_memory: ChatMemory = await chat.memory.update_memory(
            new_message_text=content.text, new_message_token_count=num_tokens, role=role.value
        )
        await update_chat_memory(chat=chat, memory=updated_chat_memory)

        return message


message_ops = MessageModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Message,
    redis=None,
)

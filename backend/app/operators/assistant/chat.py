from typing import Dict

from tkhelper.models import ModelEntity, RedisOperator
from tkhelper.models.operator.postgres_operator import PostgresModelOperator

from app.database import redis_conn, postgres_pool
from app.models import Chat, Assistant, ChatMemory
from .assistant import assistant_ops

__all__ = ["chat_ops"]


class ChatModelOperator(PostgresModelOperator):
    async def create(self, create_dict: Dict, **kwargs) -> ModelEntity:
        kwargs = self._check_kwargs(object_id_required=None, **kwargs)
        assistant_id = kwargs.get("assistant_id")
        name = create_dict.get("name", "")
        metadata = create_dict.get("metadata", {})

        async with self.postgres_pool.get_db_connection() as conn:
            async with conn.transaction():
                # validate assistant
                assistant: Assistant = await assistant_ops.get(
                    postgres_conn=conn,
                    assistant_id=assistant_id,
                )

                # initialize chat memory
                chat_memory: ChatMemory = assistant.memory.init_chat_memory()

                # create chat
                chat = await self._create_entity(
                    conn,
                    create_dict={
                        "memory": chat_memory.model_dump(),
                        "name": name,
                        "metadata": metadata,
                    },
                    **kwargs,
                )

                # update assistant num_chats
                await assistant_ops.update(
                    postgres_conn=conn,
                    assistant_id=assistant_id,
                    update_dict={"num_chats": assistant.num_chats + 1},
                )

        return chat

    async def delete(self, **kwargs) -> ModelEntity:
        kwargs = self._check_kwargs(object_id_required=True, **kwargs)
        assistant_id = kwargs.get("assistant_id")
        chat_id = kwargs.get("chat_id")

        async with self.postgres_pool.get_db_connection() as conn:
            async with conn.transaction():
                # get assistant
                assistant = await assistant_ops.get(
                    postgres_conn=conn,
                    assistant_id=assistant_id,
                )

                # get chat
                chat = await self.get(
                    postgres_conn=conn,
                    assistant_id=assistant_id,
                    chat_id=chat_id,
                )

                # delete chat
                await self._delete_entity(conn, chat)

                # update assistant num_chats
                await assistant_ops.update(
                    postgres_conn=conn,
                    assistant_id=assistant_id,
                    update_dict={"num_chats": assistant.num_chats - 1},
                )

        return assistant


chat_ops = ChatModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Chat,
    redis=RedisOperator(
        entity_class=Chat,
        redis_conn=redis_conn,
        expire=60 * 10,  # 10 minutes
    ),
)

from common.models import Chat
from common.database.redis import redis_object_set_int, redis_object_get_int


async def set_chat_lock(assistant_id: str, chat_id: str, lock: bool):
    """
    Set chat lock
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param lock: the lock value, True or False
    :return:
    """

    await redis_object_set_int(Chat, key=f"{assistant_id}:{chat_id}:lock", value=int(lock))


async def is_chat_locked(assistant_id: str, chat_id: str) -> bool:
    """
    Is chat locked
    :param assistant: the assistant id
    :param chat_id : the chat id
    :return: True or False, indicating whether the chat is locked
    """

    return await redis_object_get_int(Chat, key=f"{assistant_id}:{chat_id}:lock") == 1

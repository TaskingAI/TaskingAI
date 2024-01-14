from common.models import Message, Chat


async def get_message(conn, chat: Chat, message_id: str):
    # 1. get from db
    row = await conn.fetchrow(
        "SELECT * FROM message WHERE assistant_id = $1 AND chat_id = $2 AND message_id = $3",
        chat.assistant_id,
        chat.chat_id,
        message_id,
    )

    # 2. return if exists
    if row:
        message = Message.build(row)
        return message

    return None

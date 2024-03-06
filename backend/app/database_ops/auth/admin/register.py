import logging
import bcrypt

from app.database.connection import postgres_pool
from app.models import Admin
from .refresh_token import generate_token
from app.operators import admin_ops

logger = logging.getLogger(__name__)


def _generate_password_hash(password: str):
    # Create a random salt
    salt_bytes = bcrypt.gensalt()
    # Convert byte type salt to string type
    salt_str = salt_bytes.decode("utf-8")
    # Hash the password using salt
    password_hash_bytes = bcrypt.hashpw(password.encode("utf-8"), salt_bytes)
    # Convert byte type hash password to string type
    password_hash_str = password_hash_bytes.decode("utf-8")
    return salt_str, password_hash_str


async def register_admin(username: str, password: str) -> Admin:
    admin_id = Admin.generate_random_id()
    salt, password_hash = _generate_password_hash(password)
    token = generate_token(admin_id, [])

    # 1. create admin in database
    async with postgres_pool.get_db_connection() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                """
                INSERT INTO app_admin (admin_id, username, password_hash, salt, token)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
            """,
                admin_id,
                username,
                password_hash,
                salt,
                token,
            )

    # 2. write to redis and return
    admin = Admin.build(row)
    await admin_ops.redis.set(admin)

    logger.info(f"Registered admin {username}")

    return admin

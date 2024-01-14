from common.database.postgres.pool import postgres_db_pool
from common.models import Assistant
from .get import get_assistant
from typing import Dict, List
import json
import logging

logger = logging.getLogger(__name__)


async def create_assistant(
    model_id: str,
    name: str,
    description: str,
    system_prompt_template: List[str],
    memory: Dict,
    tools: List,
    tool_configs: Dict,
    retrievals: List,
    retrieval_configs: Dict,
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
    :param tool_configs: the assistant tool configs
    :param retrievals: the assistant retrievals, a list of tuple (type, id)
    :param retrieval_configs: the assistant retrieval configs
    :param metadata: the assistant metadata
    """

    new_id = Assistant.generate_random_id()

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert the assistant into database
            await conn.execute(
                """
                INSERT INTO assistant (assistant_id, name, description, model_id,
                system_prompt_template, memory, tools, tool_configs,
                retrievals, retrieval_configs, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
                new_id,
                name,
                description,
                model_id,
                json.dumps(system_prompt_template),
                json.dumps(memory),
                json.dumps(tools),
                json.dumps(tool_configs),
                json.dumps(retrievals),
                json.dumps(retrieval_configs),
                json.dumps(metadata),
            )

    # 2. get and add to redis
    assistant = await get_assistant(new_id)
    return assistant

from common.models import Record, RecordType, Status
from .get import get_record
from typing import Dict, List
import json


async def create_record(
    postgres_conn,
    collection_id: str,
    type: RecordType,
    content: str,
    metadata: Dict[str, str],
) -> List[Record]:
    """
    Create record
    :param postgres_conn: postgres connection
    :param collection_id: the collection id
    :param type: the record type
    :param content: the record content
    :param metadata: the record metadata
    :return: the created record
    """

    new_id = Record.generate_random_id()

    # 1. insert into database
    await postgres_conn.execute(
        """
        INSERT INTO record (record_id, collection_id, type, content, status, metadata)
        VALUES ($1, $2, $3, $4, $5, $6);
    """,
        new_id,
        collection_id,
        type.value,
        content,
        Status.READY.value,
        json.dumps(metadata),
    )

    # 2. get and add to redis
    record = await get_record(postgres_conn, new_id)
    return record

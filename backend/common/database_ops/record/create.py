from common.models import Collection, Record, RecordType, Status
from .get import get_record
from typing import Dict
import json


async def create_record(
    postgres_conn,
    collection: Collection,
    title: str,
    type: RecordType,
    content: str,
    metadata: Dict[str, str],
) -> Record:
    """
    Create record
    :param postgres_conn: postgres connection
    :param collection: the collection where the record belongs to
    :param title: the record title
    :param type: the record type
    :param content: the record content
    :param metadata: the record metadata
    :return: the created record
    """

    new_id = Record.generate_random_id()

    # 1. insert into database
    await postgres_conn.execute(
        """
        INSERT INTO record (record_id, collection_id, title, type, content, status, metadata)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """,
        new_id,
        collection.collection_id,
        title,
        type.value,
        content,
        Status.READY.value,
        json.dumps(metadata),
    )

    # 2. get and return
    record = await get_record(postgres_conn, collection=collection, record_id=new_id)

    return record

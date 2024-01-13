from common.models.record import Record


async def delete_record(postgres_conn, record: Record):
    # 1. delete from db
    await postgres_conn.execute(
        "DELETE FROM record WHERE collection_id=$1 AND record_id=$2;", record.collection_id, record.record_id
    )

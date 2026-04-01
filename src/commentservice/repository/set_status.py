from asyncpg import Pool
from pypika import Parameter, PostgreSQLQuery, Table


async def set_status(db_pool: Pool, comment_id: int, status: str) -> bool:
    comments = Table("comments")

    query = (
        PostgreSQLQuery.update(comments)  # type: ignore[operator]
        .set(comments.status, Parameter("$1"))
        .where(comments.id == Parameter("$2"))
        .returning(comments.id)
    )

    try:
        async with db_pool.acquire() as conn:
            updated_id = await conn.fetchval(
                query.get_sql(),
                status,
                comment_id,
            )
            return updated_id is not None
    except Exception:
        return False

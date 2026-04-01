from asyncpg import Pool
from pypika import Parameter, PostgreSQLQuery, Table

from commentservice.repository.model import CommentStatus


async def update_comment_status(
    db_pool: Pool, comment_id: int, is_flagged: bool
) -> bool:
    comments = Table("comments")
    status = (
        CommentStatus.HIDDEN.value
        if is_flagged
        else CommentStatus.APPROVED.value
    )

    query = (
        PostgreSQLQuery.update(comments)  # type: ignore[operator]
        .set(comments.status, Parameter("$1"))
        .where(comments.id == Parameter("$2"))
        .returning(comments.id)
    )

    async with db_pool.acquire() as conn:
        updated_id = await conn.fetchval(
            query.get_sql(),
            status,
            comment_id,
        )
        return updated_id is not None

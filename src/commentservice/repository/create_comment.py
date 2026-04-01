from typing import cast

from asyncpg import Pool
from pypika import Parameter, PostgreSQLQuery, Table


async def create_comment(
    db_pool: Pool, mod_id: int, author_id: int, text: str
) -> int:
    comments = Table("comments")

    query = (
        PostgreSQLQuery.into(comments)  # type: ignore[operator]
        .columns(comments.mod_id, comments.author_id, comments.text)
        .insert(Parameter("$1"), Parameter("$2"), Parameter("$3"))
        .returning(comments.id)
    )

    async with db_pool.acquire() as conn:
        comment_id = await conn.fetchval(
            query.get_sql(), mod_id, author_id, text
        )
        return cast(int, comment_id)

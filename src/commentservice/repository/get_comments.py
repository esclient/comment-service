from asyncpg import Pool
from pypika import Parameter, PostgreSQLQuery, Table

from commentservice.repository.model import Comment


async def get_comments(db_pool: Pool, mod_id: int) -> list[Comment]:
    comments = Table("comments")

    query = (
        PostgreSQLQuery.from_(comments)
        .select(
            comments.id,
            comments.author_id,
            comments.text,
            comments.created_at,
            comments.edited_at,
            comments.status,
        )
        .where(comments.mod_id == Parameter("$1"))
    )

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query.get_sql(), mod_id)
        return [Comment(**row) for row in rows]

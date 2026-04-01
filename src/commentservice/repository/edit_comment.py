from asyncpg import Pool
from pypika import Parameter, PostgreSQLQuery, Table, functions


async def edit_comment(db_pool: Pool, comment_id: int, text: str) -> bool:
    comments = Table("comments")

    query = (
        PostgreSQLQuery.update(comments)  # type: ignore[operator]
        .set(comments.text, Parameter("$1"))
        .set(
            comments.edited_at,
            functions.Now(),  # type: ignore[no-untyped-call]
        )
        .where(comments.id == Parameter("$2"))
        .returning(comments.id)
    )

    async with db_pool.acquire() as conn:
        updated_id = await conn.fetchval(query.get_sql(), text, comment_id)
        return updated_id is not None

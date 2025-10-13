from asyncpg import Pool

from commentservice.repository.model import Comment


async def get_comments(db_pool: Pool, mod_id: int) -> list[Comment]:
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, author_id, text, created_at, edited_at
            FROM comments
            WHERE mod_id = $1
            """,
            mod_id,
        )

        return [Comment(**row) for row in rows]

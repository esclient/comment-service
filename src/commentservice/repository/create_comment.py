from asyncpg import Pool


async def create_comment(
    db_pool: Pool, mod_id: int, author_id: int, text: str
) -> int:
    async with db_pool.acquire() as conn:
        comment_id = await conn.fetchval(
            """
            INSERT INTO comments (mod_id, author_id, text)
            VALUES ($1, $2, $3)
            RETURNING id
            """,
            mod_id, author_id, text
        )
        return comment_id

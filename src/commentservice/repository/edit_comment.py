from asyncpg import Pool


async def edit_comment(db_pool: Pool, comment_id: int, text: str) -> bool:
    async with db_pool.acquire() as conn:
        updated_id = await conn.fetchval(
            """
            UPDATE comments
            SET text = $1, edited_at = NOW()
            WHERE id = $2
            RETURNING id
            """,
            text,
            comment_id,
        )

        return updated_id is not None

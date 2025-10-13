from asyncpg import Pool


async def delete_comment(db_pool: Pool, comment_id: int) -> bool:
    async with db_pool.acquire() as conn:
        deleted_id = await conn.fetchval(
            """
            DELETE FROM comments
            WHERE id = $1
            RETURNING id
            """,
            comment_id,
        )

        return deleted_id is not None

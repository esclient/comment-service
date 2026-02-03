from asyncpg import Pool


async def update_comment_status(db_pool: Pool, comment_id: int, is_flagged: bool) -> bool:
    if is_flagged:
        status = 'HIDDEN'
    else:
        status = 'APPROVED'
    
    async with db_pool.acquire() as conn:
        updated_id = await conn.fetchval(
            """
            UPDATE comments
            SET status = $1
            WHERE id = $2
            RETURNING id
            """,
            status,
            comment_id,
        )

        return updated_id is not None
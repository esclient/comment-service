from asyncpg import Pool


async def set_status(db_pool: Pool, comment_id: int, status: str) -> bool:
    try:
        async with db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE comments
                SET status = $1
                WHERE id = $2
                """,
                status,
                comment_id,
            )
            rows_affected = int(result.split()[-1]) if result else 0
            return rows_affected > 0
    except Exception:
        return False

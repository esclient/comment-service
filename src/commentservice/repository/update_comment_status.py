from asyncpg import Pool
from commentservice.repository.statuses import CommentStatus

async def update_comment_status(db_pool: Pool, comment_id: int, is_flagged: bool) -> bool:
    if is_flagged:
        status = CommentStatus.HIDDEN.value
    else:
        status = CommentStatus.APPROVED.value
    
    async with db_pool.acquire() as conn:
        updated_id = await conn.fetchval(
            """
            UPDATE comments
            SET status = $1::comment_status
            WHERE id = $2
            RETURNING id
            """, 
            status, 
            comment_id
        )
        return updated_id is not None
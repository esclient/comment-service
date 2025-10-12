import asyncio
import asyncpg
from typing import List

from psycopg2.pool import ThreadedConnectionPool

from commentservice.repository.create_comment import (
    create_comment as _create_comment,
)
from commentservice.repository.delete_comment import (
    delete_comment as _delete_comment,
)
from commentservice.repository.edit_comment import (
    edit_comment as _edit_comment,
)
from commentservice.repository.get_comments import (
    get_comments as _get_comments,
)
from commentservice.repository.model import Comment


class CommentRepository:
    def __init__(self, db_pool: asyncpg.Pool):
        self._db_pool: asyncpg.Pool = db_pool

    async def close(self):
        await self._db_pool.close()

    async def create_comment(self, mod_id: int, author_id: int, text: str) -> int:
        return await _create_comment(self._db_pool, mod_id, author_id, text)

    async def edit_comment(self, comment_id: int, new_text: str) -> bool:
        return await _edit_comment(self._db_pool, comment_id, new_text)

    async def delete_comment(self, comment_id: int) -> bool:
        return await _delete_comment(self._db_pool, comment_id)

    async def get_comments(self, mod_id: int) -> List[Comment]:
        return await _get_comments(self._db_pool, mod_id)

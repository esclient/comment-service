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


class CommentRepository:
    def __init__(self, db_pool: ThreadedConnectionPool):
        self._db_pool = db_pool

    def create_comment(self, mod_id: int, author_id: int, text: str) -> int:
        return _create_comment(self._db_pool, mod_id, author_id, text)

    def edit_comment(self, comment_id: int, new_text: str) -> bool:
        return _edit_comment(self._db_pool, comment_id, new_text)

    def delete_comment(self, comment_id: int) -> bool:
        return _delete_comment(self._db_pool, comment_id)

    def get_comments(self, mod_id: int) -> tuple:
        return _get_comments(self._db_pool, mod_id)

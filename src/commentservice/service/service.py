from commentservice.repository.model import Comment
from commentservice.repository.repository import CommentRepository
from commentservice.service.create_comment import (
    create_comment as _create_comment,
)
from commentservice.service.edit_comment import edit_comment as _edit_comment
from commentservice.service.get_comments import get_comments as _get_comments
from commentservice.service.set_status import set_status as _set_status


class CommentService:
    def __init__(self, repo: CommentRepository):
        self._repo = repo

    async def create_comment(
        self, mod_id: int, author_id: int, text: str
    ) -> int:
        return await _create_comment(self._repo, mod_id, author_id, text)

    async def edit_comment(self, comment_id: int, new_text: str) -> bool:
        return await _edit_comment(self._repo, comment_id, new_text)

    async def set_status(self, comment_id: int, status: str) -> bool:
        return await _set_status(self._repo, comment_id, status)

    async def get_comments(self, mod_id: int) -> list[Comment]:
        return await _get_comments(self._repo, mod_id)

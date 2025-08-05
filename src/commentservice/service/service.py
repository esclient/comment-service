from commentservice.repository.model import Comment
from commentservice.repository.repository import CommentRepository
from commentservice.service.create_comment import (
    create_comment as _create_comment,
)
from commentservice.service.delete_comment import (
    delete_comment as _delete_comment,
)
from commentservice.service.edit_comment import edit_comment as _edit_comment
from commentservice.service.get_comments import get_comments as _get_comments


class CommentService:
    def __init__(self, repo: CommentRepository):
        self._repo = repo

    def create_comment(self, mod_id: int, author_id: int, text: str) -> int:
        return _create_comment(self._repo, mod_id, author_id, text)

    def edit_comment(self, comment_id: int, new_text: str) -> bool:
        return _edit_comment(self._repo, comment_id, new_text)

    def delete_comment(self, comment_id: int) -> bool:
        return _delete_comment(self._repo, comment_id)

    def get_comments(self, mod_id: int) -> list[Comment]:
        return _get_comments(self._repo, mod_id)

from commentservice.repository.repository import CommentRepository


def edit_comment(repo: CommentRepository, comment_id: int, text: str) -> bool:
    return repo.edit_comment(comment_id, text)

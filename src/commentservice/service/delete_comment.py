from commentservice.repository.repository import CommentRepository


def delete_comment(repo: CommentRepository, comment_id: int) -> bool:
    return repo.delete_comment(comment_id)

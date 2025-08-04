from commentservice.repository.repository import CommentRepository


def get_comments(repo: CommentRepository, mod_id: int) -> tuple:
    return repo.get_comments(mod_id)

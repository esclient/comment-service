from commentservice.repository.repository import CommentRepository


def create_comment(
    repo: CommentRepository, mod_id: int, author_id: int, text: str
) -> int:
    return repo.create_comment(mod_id, author_id, text)

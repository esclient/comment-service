from commentservice.repository.model import Comment
from commentservice.repository.repository import CommentRepository


async def get_comments(repo: CommentRepository, mod_id: int) -> list[Comment]:
    return await repo.get_comments(mod_id)

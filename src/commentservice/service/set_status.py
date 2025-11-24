from commentservice.repository.repository import CommentRepository


async def set_status(repo: CommentRepository, comment_id: int, status: str) -> bool:
    return await repo.set_status(comment_id, status)

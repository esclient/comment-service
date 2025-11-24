from commentservice.repository.repository import CommentRepository


async def edit_comment(repo: CommentRepository, comment_id: int, text: str) -> bool:
    return await repo.edit_comment(comment_id, text)

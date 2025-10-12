from commentservice.repository.repository import CommentRepository


async def delete_comment(repo: CommentRepository, comment_id: int) -> bool:
    return await repo.delete_comment(comment_id)

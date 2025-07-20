from commentservice.repository.delete_comment import delete_comments as repo_delete_comments

def delete_comments(comments_id: int) -> int:
    return repo_delete_comments(comments_id)
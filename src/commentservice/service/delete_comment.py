from commentservice.repository.delete_comment import delete_comment as repo_delete_comment

def delete_comment(comment_id: int) -> int:
    return repo_delete_comment(comment_id)
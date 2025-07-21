from commentservice.repository.edit_comment import (
    edit_comment as repo_edit_comment,
)

def edit_comment(comment_id: int, text: str) -> bool:
    return repo_edit_comment(comment_id, text)

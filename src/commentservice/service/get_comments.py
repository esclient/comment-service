from commentservice.repository.get_comments import (
    get_comments as repo_get_comments
)

def get_comments(mod_id: int) -> int:

    return repo_get_comments(mod_id)

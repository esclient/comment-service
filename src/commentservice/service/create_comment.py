from commentservice.repository.create_comment import create_comment as repo_create_comment

def create_comment(mod_id: int, author_id: int, text: str) -> int:
    return repo_create_comment(mod_id, author_id, text)
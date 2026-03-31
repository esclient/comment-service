from dataclasses import dataclass
from datetime import datetime
from commentservice.repository.statuses import CommentStatus

@dataclass
class Comment:
    id: int
    author_id: int
    text: str
    created_at: datetime
    edited_at: datetime | None
    status: CommentStatus
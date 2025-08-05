from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comment:
    id: int
    author_id: int
    text: str
    created_at: datetime
    edited_at: datetime | None

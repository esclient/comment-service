from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class CommentStatus(StrEnum):
    DELETED = "DELETED"
    HIDDEN = "HIDDEN"
    APPROVED = "APPROVED"
    ON_MODERATION = "ON_MODERATION"


@dataclass
class Comment:
    id: int
    author_id: int
    text: str
    created_at: datetime
    edited_at: datetime | None
    status: CommentStatus

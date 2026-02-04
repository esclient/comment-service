from enum import Enum

class CommentStatus(str, Enum):
    DELETED = "DELETED"
    HIDDEN = "HIDDEN"
    APPROVED = "APPROVED"
    ON_MODERATION = "ON_MODERATION"
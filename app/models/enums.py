from enum import Enum

class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"

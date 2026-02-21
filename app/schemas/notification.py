# app/schemas/notifications.py
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"


class NotificationCreateIn(BaseModel):
    type: NotificationType
    text: str = Field(min_length=1, max_length=10_000)


class NotificationOut(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    text: str
    created_at: datetime

    username: str
    avatar_url: str

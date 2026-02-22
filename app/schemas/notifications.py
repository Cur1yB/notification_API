from datetime import datetime
from app.models.enums import NotificationType
from pydantic import BaseModel, Field


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

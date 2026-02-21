from tortoise import Model, fields
from typing import TYPE_CHECKING
from datetime import datetime
from app.models.enums import NotificationType
if TYPE_CHECKING:
    from app.models.users import User

class Notification(Model):
    id: int = fields.IntField(primary_key=True)
    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        to='models.User',
        related_name="notifications",
        on_delete=fields.CASCADE,
        db_index=True
    )
    type: str = fields.CharEnumField(
        NotificationType,
        max_length=20
    )
    text: str = fields.TextField()
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "notifications"


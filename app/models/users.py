from tortoise import Model, fields
from datetime import datetime

class User(Model):
    id: int = fields.IntField(primary_key=True)
    username: str = fields.CharField(
        max_length = 100,
        unique=True,
        null=False
    )
    password_hash: str = fields.CharField(
        max_length = 255,
        null=False
    )
    avatar_url: str = fields.CharField(
        max_length=512,
        default='...'
    )
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

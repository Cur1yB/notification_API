from app.models.notifications import Notification
from app.schemas.notifications import NotificationOut


async def create_notification_db(
    *, user_id: int, type_: str, text: str
) -> Notification:
    return await Notification.create(user_id=user_id, type=type_, text=text)


async def list_notifications_db(
    *, user_id: int, limit: int, offset: int
) -> list[Notification]:
    return (
        await Notification.filter(user_id=user_id)
        .select_related("user")
        .order_by("-created_at")
        .limit(limit)
        .offset(offset)
    )


async def get_notification_db(*, notification_id: int) -> Notification | None:
    return await Notification.filter(id=notification_id).first()


async def delete_notification_db(*, notification: Notification) -> None:
    await notification.delete()


def _to_out(n) -> NotificationOut:
    return NotificationOut(
        id=n.id,
        user_id=n.user_id,
        type=n.type,
        text=n.text,
        created_at=n.created_at,
        username=n.user.username,
        avatar_url=n.user.avatar_url,
    )

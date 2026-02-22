from app.exceptions import ForbiddenNotificationAccess
from app.models.notifications import Notification
from app.schemas.notification import NotificationOut


async def create_notification_db(*, user_id: int, type_: str, text: str) -> Notification:
    return await Notification.create(user_id=user_id, type=type_, text=text)


async def list_notifications_db(*, user_id: int, limit: int, offset: int) -> list[Notification]:
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


async def create_notification(*, user_id: int, type_: str, text: str) -> NotificationOut:
    n = await create_notification_db(user_id=user_id, type_=type_, text=text)
    await n.fetch_related("user")
    return _to_out(n)


async def list_notifications(*, user_id: int, limit: int, offset: int) -> list[NotificationOut]:
    items = await list_notifications_db(user_id=user_id, limit=limit, offset=offset)
    return [_to_out(n) for n in items]


async def delete_notification(*, user_id: int, notification_id: int) -> None:
    n = await get_notification_db(notification_id=notification_id)
    if not n:
        raise KeyError("Notification not found")

    if n.user_id != user_id:
        raise ForbiddenNotificationAccess()

    await delete_notification_db(notification=n)

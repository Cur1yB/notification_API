from app.db_services.notifications import (
    _to_out,
    create_notification_db,
    delete_notification_db,
    get_notification_db,
    list_notifications_db,
)
from app.exceptions import ForbiddenNotificationAccess
from app.schemas.notifications import NotificationOut


async def create_notification(
    *, user_id: int, type_: str, text: str
) -> NotificationOut:
    n = await create_notification_db(user_id=user_id, type_=type_, text=text)
    await n.fetch_related("user")
    return _to_out(n)


async def list_notifications(
    *, user_id: int, limit: int, offset: int
) -> list[NotificationOut]:
    items = await list_notifications_db(user_id=user_id, limit=limit, offset=offset)
    return [_to_out(n) for n in items]


async def delete_notification(*, user_id: int, notification_id: int) -> None:
    n = await get_notification_db(notification_id=notification_id)
    if not n:
        raise KeyError("Notification not found")

    if getattr(n, "user_id") != user_id:
        raise ForbiddenNotificationAccess()

    await delete_notification_db(notification=n)

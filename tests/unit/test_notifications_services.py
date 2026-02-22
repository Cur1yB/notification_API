import pytest
from app.models.notifications import Notification
from app.services.notifications import (
    create_notification,
    list_notifications,
    delete_notification,
)
from app.exceptions import ForbiddenNotificationAccess

@pytest.mark.asyncio
async def test_create_notification(user):
    notif = await create_notification(user_id=user.id, type_="like", text="Hello!")
    assert notif.user_id == user.id
    assert notif.type == "like"
    assert notif.text == "Hello!"
    assert notif.username == "pupalupa"
    assert hasattr(notif, "created_at")
    assert notif.avatar_url == user.avatar_url

@pytest.mark.asyncio
async def test_list_notifications(user):
    await create_notification(user_id=user.id, type_="comment", text="Msg1")
    await create_notification(user_id=user.id, type_="comment", text="Msg2")
    lst = await list_notifications(user_id=user.id, limit=10, offset=0)
    assert len(lst) >= 2

    for notif in lst:
        assert notif.user_id == user.id

@pytest.mark.asyncio
async def test_delete_notification(user, other_user):
    notif = await create_notification(user_id=user.id, type_="repost", text="DelMe")
    await delete_notification(user_id=user.id, notification_id=notif.id)
    assert await Notification.filter(id=notif.id).count() == 0

    notif2 = await create_notification(user_id=user.id, type_="repost", text="CantDelMe")
    with pytest.raises(ForbiddenNotificationAccess):
        await delete_notification(user_id=other_user.id, notification_id=notif2.id)

@pytest.mark.asyncio
async def test_delete_nonexistent(user):
    with pytest.raises(KeyError):
        await delete_notification(user_id=user.id, notification_id=999999)

import pytest

from app.models.notifications import Notification
from app.security import create_token
from app.settings import settings

pytestmark = pytest.mark.asyncio


def _auth_headers_for_user(user_id: int) -> dict[str, str]:
    token = create_token(
        user_id=user_id,
        token_type="access",
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        ttl_seconds=settings.ACCESS_TTL_SECONDS,
    )
    return {"Authorization": f"Bearer {token}"}


async def test_create_notification_ok(client, user):
    payload = {"type": "like", "text": "Hello!"}
    headers = _auth_headers_for_user(user.id)

    r = await client.post("/notifications/", json=payload, headers=headers)
    assert r.status_code == 201, r.text

    data = r.json()
    assert data["user_id"] == user.id
    assert data["type"] == "like"
    assert data["text"] == "Hello!"
    assert data["username"] == user.username
    assert "created_at" in data


async def test_list_notifications_only_own(client, user, other_user):
    await Notification.create(user_id=user.id, type="like", text="U1")
    await Notification.create(user_id=user.id, type="comment", text="U2")
    await Notification.create(user_id=other_user.id, type="repost", text="OTHER")

    headers = _auth_headers_for_user(user.id)

    r = await client.get("/notifications/?limit=10&offset=0", headers=headers)
    assert r.status_code == 200, r.text

    items = r.json()
    assert isinstance(items, list)
    assert len(items) == 2
    assert {x["text"] for x in items} == {"U1", "U2"}
    assert all(x["user_id"] == user.id for x in items)


async def test_list_notifications_pagination(client, user):
    await Notification.create(user_id=user.id, type="like", text="A")
    await Notification.create(user_id=user.id, type="like", text="B")
    await Notification.create(user_id=user.id, type="like", text="C")

    headers = _auth_headers_for_user(user.id)

    r1 = await client.get("/notifications/?limit=2&offset=0", headers=headers)
    assert r1.status_code == 200
    page1 = r1.json()
    assert len(page1) == 2

    r2 = await client.get("/notifications/?limit=2&offset=2", headers=headers)
    assert r2.status_code == 200
    page2 = r2.json()
    assert len(page2) == 1


async def test_delete_notification_ok_only_own(client, user, other_user):
    n1 = await Notification.create(user_id=user.id, type="like", text="DEL")
    headers_user = _auth_headers_for_user(user.id)

    r = await client.delete(f"/notifications/{n1.id}", headers=headers_user)
    assert r.status_code == 204, r.text
    assert await Notification.filter(id=n1.id).count() == 0

    n2 = await Notification.create(user_id=other_user.id, type="like", text="OTHER")
    r2 = await client.delete(f"/notifications/{n2.id}", headers=headers_user)
    assert r2.status_code == 403, r2.text
    assert await Notification.filter(id=n2.id).count() == 1


async def test_delete_notification_not_found(client, user):
    headers = _auth_headers_for_user(user.id)
    r = await client.delete("/notifications/999999", headers=headers)
    assert r.status_code == 404, r.text


async def test_notifications_require_auth(client):
    r = await client.get("/notifications/")
    assert r.status_code in (401, 403), r.text

    r2 = await client.post("/notifications/", json={"type": "like", "text": "x"})
    assert r2.status_code in (401, 403), r2.text

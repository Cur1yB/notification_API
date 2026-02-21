import pytest

from app.exceptions import AuthError, UserAlreadyExists
from app.services.auth import register_user, login_user, refresh_access_token


class DummySettings:
    DEFAULT_AVATAR_URL = "https://example.com/a.png"
    JWT_SECRET = "test-secret"
    JWT_ALG = "HS256"
    ACCESS_TTL_SECONDS = 60
    REFRESH_TTL_SECONDS = 3600


class DummyUser:
    def __init__(self, user_id: int, username: str = "u", password_hash: str = "hash"):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash


@pytest.mark.asyncio
async def test_register_user_ok(monkeypatch):
    async def fake_get_by_username(*, username: str):
        return None

    async def fake_create_user(*, username: str, password_hash: str, avatar_url: str):
        assert username == "alex"
        assert avatar_url == DummySettings.DEFAULT_AVATAR_URL
        assert password_hash == "HASHED"
        return DummyUser(1, username=username, password_hash=password_hash)

    def fake_hash_password(password: str) -> str:
        assert password == "pass12345"
        return "HASHED"

    def fake_create_token(**kwargs) -> str:
        # return distinct tokens based on type
        return f"TOKEN-{kwargs['token_type']}-{kwargs['user_id']}"

    monkeypatch.setattr("app.services.auth.get_by_username", fake_get_by_username)
    monkeypatch.setattr("app.services.auth.create_user", fake_create_user)
    monkeypatch.setattr("app.services.auth.hash_password", fake_hash_password)
    monkeypatch.setattr("app.services.auth.create_token", fake_create_token)

    res = await register_user(username="alex", password="pass12345", settings=DummySettings)
    assert res["user_id"] == 1
    assert res["access"] == "TOKEN-access-1"
    assert res["refresh"] == "TOKEN-refresh-1"


@pytest.mark.asyncio
async def test_register_user_username_taken(monkeypatch):
    async def fake_get_by_username(*, username: str):
        return DummyUser(99, username=username)

    monkeypatch.setattr("app.services.auth.get_by_username", fake_get_by_username)

    with pytest.raises(UserAlreadyExists):
        await register_user(username="alex", password="pass12345", settings=DummySettings)


@pytest.mark.asyncio
async def test_login_user_ok(monkeypatch):
    async def fake_get_by_username(*, username: str):
        return DummyUser(10, username=username, password_hash="HASHED")

    def fake_verify_password(password: str, password_hash: str) -> bool:
        assert password == "pass12345"
        assert password_hash == "HASHED"
        return True

    def fake_create_token(**kwargs) -> str:
        return f"TOKEN-{kwargs['token_type']}-{kwargs['user_id']}"

    monkeypatch.setattr("app.services.auth.get_by_username", fake_get_by_username)
    monkeypatch.setattr("app.services.auth.verify_password", fake_verify_password)
    monkeypatch.setattr("app.services.auth.create_token", fake_create_token)

    res = await login_user(username="alex", password="pass12345", settings=DummySettings)
    assert res["access"] == "TOKEN-access-10"
    assert res["refresh"] == "TOKEN-refresh-10"


@pytest.mark.asyncio
async def test_login_user_invalid_username(monkeypatch):
    async def fake_get_by_username(*, username: str):
        return None

    monkeypatch.setattr("app.services.auth.get_by_username", fake_get_by_username)

    with pytest.raises(AuthError):
        await login_user(username="alex", password="pass12345", settings=DummySettings)


@pytest.mark.asyncio
async def test_login_user_invalid_password(monkeypatch):
    async def fake_get_by_username(*, username: str):
        return DummyUser(10, username=username, password_hash="HASHED")

    def fake_verify_password(password: str, password_hash: str) -> bool:
        return False

    monkeypatch.setattr("app.services.auth.get_by_username", fake_get_by_username)
    monkeypatch.setattr("app.services.auth.verify_password", fake_verify_password)

    with pytest.raises(AuthError):
        await login_user(username="alex", password="wrong", settings=DummySettings)


@pytest.mark.asyncio
async def test_refresh_access_token_ok(monkeypatch):
    def fake_decode_token(*, token: str, secret: str, algorithm: str):
        assert token == "REFRESH"
        assert secret == DummySettings.JWT_SECRET
        assert algorithm == DummySettings.JWT_ALG
        return {"sub": "7", "type": "refresh"}

    def fake_create_token(**kwargs) -> str:
        assert kwargs["token_type"] == "access"
        assert kwargs["user_id"] == 7
        return "NEW-ACCESS"

    monkeypatch.setattr("app.services.auth.decode_token", fake_decode_token)
    monkeypatch.setattr("app.services.auth.create_token", fake_create_token)

    res = await refresh_access_token(refresh_token="REFRESH", settings=DummySettings)
    assert res == {"access": "NEW-ACCESS"}


@pytest.mark.asyncio
async def test_refresh_access_token_wrong_type(monkeypatch):
    def fake_decode_token(*, token: str, secret: str, algorithm: str):
        return {"sub": "7", "type": "access"}  # wrong

    monkeypatch.setattr("app.services.auth.decode_token", fake_decode_token)

    with pytest.raises(AuthError):
        await refresh_access_token(refresh_token="ANY", settings=DummySettings)
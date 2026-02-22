import pytest


@pytest.mark.anyio
async def test_register_ok(client):
    password = "mclover777"
    r = await client.post(
        "/auth/register",
        json={"username": "PiPiSA", "password": password},
    )
    assert r.status_code == 200, r.text
    data = r.json()

    assert "user_id" in data
    assert "access" in data
    assert "refresh" in data

    assert isinstance(data["user_id"], int)
    assert isinstance(data["access"], str) and data["access"]
    assert isinstance(data["refresh"], str) and data["refresh"]


@pytest.mark.anyio
async def test_register_conflict_username_taken(client):
    r1 = await client.post(
        "/auth/register", json={"username": "PiPiSA", "password": "mclover777"}
    )
    assert r1.status_code == 200

    r2 = await client.post(
        "/auth/register", json={"username": "PiPiSA", "password": "mclover777"}
    )
    assert r2.status_code == 409, r2.text


@pytest.mark.anyio
async def test_login_ok(client):
    await client.post(
        "/auth/register", json={"username": "PiPiSA", "password": "mclover777"}
    )

    r = await client.post(
        "/auth/login", json={"username": "PiPiSA", "password": "mclover777"}
    )
    assert r.status_code == 200, r.text
    data = r.json()

    assert "access" in data and data["access"]
    assert "refresh" in data and data["refresh"]


@pytest.mark.anyio
async def test_login_wrong_password(client):
    await client.post(
        "/auth/register", json={"username": "PiPiSA", "password": "mclover777"}
    )

    r = await client.post(
        "/auth/login", json={"username": "PiPiSA", "password": "SitOnMyFacePlease "}
    )
    assert r.status_code == 401, r.text


@pytest.mark.anyio
async def test_refresh_ok(client):
    reg = await client.post(
        "/auth/register", json={"username": "PiPiSA", "password": "mclover777"}
    )
    refresh = reg.json()["refresh"]
    r = await client.post("/auth/refresh", json={"refresh": refresh})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access" in data and data["access"]


@pytest.mark.anyio
async def test_refresh_rejects_access_token(client):
    reg = await client.post(
        "/auth/register", json={"username": "PiPiSA", "password": "mclover777"}
    )
    access = reg.json()["access"]

    r = await client.post("/auth/refresh", json={"refresh": access})
    assert r.status_code == 401, r.text


@pytest.mark.anyio
async def test_refresh_invalid_token(client):
    r = await client.post("/auth/refresh", json={"refresh": "XYITA"})
    assert r.status_code == 401, r.text

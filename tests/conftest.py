import os
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise
from app.main import app
from dotenv import load_dotenv

from app.models.users import User

load_dotenv()


TEST_DB_URL = os.getenv("TEST_DATABASE_URL")


@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db():
    db_url = os.environ.get("DATABASE_URL")
    assert db_url, "DATABASE_URL is not set for tests"

    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["app.models.users", "app.models.notifications"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    from app.models.notifications import Notification
    from app.models.users import User

    await Notification.all().delete()
    await User.all().delete()
    yield


@pytest_asyncio.fixture
async def user():
    u = await User.create(username="pupalupa", password_hash="pupahash")
    yield u
    await u.delete()


@pytest_asyncio.fixture
async def other_user():
    u = await User.create(username="PiPiSA", password_hash="lupapupa")
    yield u
    await u.delete()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

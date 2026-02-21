from tortoise import Tortoise
import settings

TORTOISE_MODELS = [
    "app.models.users",
    "app.models.notifications"
]

async def init_db() -> None:
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": TORTOISE_MODELS},
    )
    await Tortoise.generate_schemas() # миграций в задании не было

async def close_db() -> None:
    await Tortoise.close_connections()
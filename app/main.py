from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.settings import settings
from app.db import (
    TORTOISE_MODELS
    
)
from app.routers.auth import router as auth_router
from app.routers.notifications import router as notifications_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.include_router(notifications_router)
app.include_router(auth_router)

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": TORTOISE_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)
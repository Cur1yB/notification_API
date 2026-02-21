from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import (
    init_db,
    close_db
)
from app.routers.auth import router as auth_router
from app.routers.notifications import router as notifications_router


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(notifications_router)
app.include_router(auth_router)
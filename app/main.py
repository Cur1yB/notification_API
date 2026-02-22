import sys
import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from loguru import logger

from app.settings import settings
from app.db import TORTOISE_MODELS
from app.routers.auth import router as auth_router
from app.routers.notifications import router as notifications_router
from tortoise.contrib.fastapi import register_tortoise


def setup_logging() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOGLEVEL,
        backtrace=False,
        diagnose=False,
        enqueue=True,
    )


setup_logging()

app = FastAPI()

app.include_router(notifications_router)
app.include_router(auth_router)


# время запроса отслеживаем, нужен LOGLEVEL=INFO в .env
@app.middleware("http")
async def access_log(request: Request, call_next: Callable) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000

    logger.info(
        "{method} {path} -> {status} ({ms:.1f}ms)",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        ms=elapsed_ms,
    )
    return response


register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": TORTOISE_MODELS},
    generate_schemas=True,  # про миграции в ТЗ не было
    add_exception_handlers=True,
)

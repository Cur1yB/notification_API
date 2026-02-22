from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jwt

from app.exceptions import AuthError, UserAlreadyExists, ForbiddenNotificationAccess


def init_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExists)
    async def user_exists_handler(request: Request, exc: UserAlreadyExists):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(AuthError)
    async def auth_error_handler(request: Request, exc: AuthError):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(jwt.ExpiredSignatureError)
    async def jwt_expired_handler(request: Request, exc: jwt.ExpiredSignatureError):
        return JSONResponse(status_code=401, content={"detail": "Token expired"})

    @app.exception_handler(jwt.InvalidTokenError)
    async def jwt_invalid_handler(request: Request, exc: jwt.InvalidTokenError):
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})
    
    @app.exception_handler(ForbiddenNotificationAccess)
    async def forbidden_notification_access_handler(request: Request, exc: ForbiddenNotificationAccess):
        return JSONResponse(status_code=403, content={"detail": "Forbidden"})
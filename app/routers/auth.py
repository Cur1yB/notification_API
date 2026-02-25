from fastapi import APIRouter, HTTPException
from app.settings import settings
from app.schemas.auth import (
    LoginIn,
    RefreshIn,
    RegisterIn,
    RegisterResponse,
    TokenPairResponse,
    AccessTokenResponse,
)
from app.services.auth import login_user, refresh_access_token, register_user
from app.exceptions import AuthError, UserAlreadyExists
from jwt import InvalidTokenError


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    summary="Register new user",
    response_model=RegisterResponse,
    description="Create user and get JWT tokens. Username must be unique.",
)
async def register(data: RegisterIn):
    try:
        user = await register_user(
            username=data.username, password=data.password, settings=settings
        )
    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail="Username already taken")
    return user


@router.post(
    "/login",
    summary="Login",
    response_model=TokenPairResponse,
    description="Get new JWT tokens using username and password.",
)
async def login(data: LoginIn):
    try:
        user = await login_user(
            username=data.username, password=data.password, settings=settings
        )
    except AuthError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


@router.post(
    "/refresh",
    summary="Refresh access token",
    response_model=AccessTokenResponse,
    description="Use refresh token for get new access token.",
)
async def refresh(data: RefreshIn):
    try:
        new_access = await refresh_access_token(
            refresh_token=data.refresh, settings=settings
        )
        return new_access
    except (AuthError, InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

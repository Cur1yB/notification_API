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
from app.services.auth import _make_tokens
from app.exceptions import AuthError
from app.models.users import User
from app.security import create_token, decode_token, hash_password, verify_password
from tortoise.exceptions import IntegrityError
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
        user = await User.create(
            username=data.username,
            password_hash=hash_password(data.password),
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username already taken")

    return {"user_id": user.id, **_make_tokens(user.id)}


@router.post(
    "/login",
    summary="Login",
    response_model=TokenPairResponse,
    description="Get new JWT tokens using username and password.",
)
async def login(data: LoginIn):
    user = await User.filter(username=data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return _make_tokens(user.id)


@router.post(
    "/refresh",
    summary="Refresh access token",
    response_model=AccessTokenResponse,
    description="Use refresh token for get new access token.",
)
async def refresh_ep(data: RefreshIn):
    try:
        payload = decode_token(
            token=data.refresh,
            secret=settings.JWT_SECRET,
            algorithm=settings.JWT_ALG,
        )
        if payload.get("type") != "refresh":
            raise AuthError("Wrong token type")

        user_id = int(payload["sub"])
        new_access = create_token(
            user_id=user_id,
            token_type="access",
            secret=settings.JWT_SECRET,
            algorithm=settings.JWT_ALG,
            ttl_seconds=settings.ACCESS_TTL_SECONDS,
        )
        return {"access": new_access}
    except (AuthError, InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

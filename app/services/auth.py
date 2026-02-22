from app.settings import settings
from app.db_services.users import get_by_username, create_user
from app.exceptions import AuthError, UserAlreadyExists
from app.security import create_token, hash_password, verify_password, decode_token
import os
import time
import jwt


async def register_user(*, username: str, password: str, settings) -> dict:
    existing = await get_by_username(username=username)
    if existing:
        raise UserAlreadyExists("Username already taken")

    user = await create_user(
        username=username,
        password_hash=hash_password(password),
        avatar_url=settings.DEFAULT_AVATAR_URL,
    )

    access = create_token(
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        token_type="access",
        user_id=user.id,
        ttl_seconds=settings.ACCESS_TTL_SECONDS,
    )
    refresh = create_token(
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        token_type="refresh",
        user_id=user.id,
        ttl_seconds=settings.REFRESH_TTL_SECONDS,
    )
    return {"user_id": user.id, "access": access, "refresh": refresh}


async def login_user(*, username: str, password: str, settings) -> dict:
    user = await get_by_username(username=username)
    if not user:
        raise AuthError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise AuthError("Invalid credentials")

    access = create_token(
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        token_type="access",
        user_id=user.id,
        ttl_seconds=settings.ACCESS_TTL_SECONDS,
    )
    refresh = create_token(
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        token_type="refresh",
        user_id=user.id,
        ttl_seconds=settings.REFRESH_TTL_SECONDS,
    )
    return {"access": access, "refresh": refresh}


async def refresh_access_token(*, refresh_token: str, settings) -> dict:
    payload = decode_token(
        token=refresh_token,
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
    )

    if payload.get("type") != "refresh":
        raise AuthError("Invalid token type")

    user_id = int(payload["sub"])

    access = create_token(
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        token_type="access",
        user_id=user_id,
        ttl_seconds=settings.ACCESS_TTL_SECONDS,
    )
    return {"access": access}


def _make_tokens(user_id: int) -> dict:
    secret = settings.JWT_SECRET
    alg = settings.JWT_ALG

    now = int(time.time())
    access_ttl = int(os.environ.get("ACCESS_TTL_SECONDS", "900"))  # 15 min
    refresh_ttl = int(os.environ.get("REFRESH_TTL_SECONDS", "604800"))  # 7 days

    access_payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + access_ttl,
    }
    refresh_payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": now + refresh_ttl,
    }

    return {
        "access": jwt.encode(access_payload, secret, algorithm=alg),
        "refresh": jwt.encode(refresh_payload, secret, algorithm=alg),
    }

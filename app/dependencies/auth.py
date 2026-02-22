from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.exceptions import AuthError
from app.security import decode_token
from app.settings import settings

bearer = HTTPBearer(auto_error=False)


async def get_current_user_id(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> int:
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(token=creds.credentials, secret=settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(payload["sub"])
    except (AuthError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
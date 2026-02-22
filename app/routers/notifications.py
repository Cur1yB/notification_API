from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies.auth import get_current_user_id
from app.exceptions import ForbiddenNotificationAccess
from app.schemas.notification import NotificationCreateIn, NotificationOut
from app.services.notifications import create_notification, delete_notification, list_notifications

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def create_notification_ep(
    data: NotificationCreateIn,
    user_id: int = Depends(get_current_user_id),
):
    return await create_notification(user_id=user_id, type_=data.type.value, text=data.text)


@router.get("/", response_model=list[NotificationOut])
async def list_notifications_ep(
    user_id: int = Depends(get_current_user_id),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return await list_notifications(user_id=user_id, limit=limit, offset=offset)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification_ep(
    notification_id: int,
    user_id: int = Depends(get_current_user_id),
):
    try:
        await delete_notification(user_id=user_id, notification_id=notification_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Notification not found")
    except ForbiddenNotificationAccess:
        raise HTTPException(status_code=403, detail="Forbidden")
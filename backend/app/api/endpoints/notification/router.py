from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)
from app.services.notification import (
    create_notification,
    get_notification,
    get_notifications,
    update_notification,
    delete_notification,
    update_notification_status,
    get_notifications_by_user_id,
)
from app.core.security import get_current_user
from app.models.notifications import NotificationStatus

router = APIRouter()


@router.post(
    "/notifications",
    response_model=NotificationResponse,
    dependencies=[Depends(get_current_user)],
)
async def create_notification_route(
    notification_in: NotificationCreate,
    db: Session = Depends(get_db),
):
    """创建通知"""
    return create_notification(db=db, notification_in=notification_in)


@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def read_notification_route(notification_id: str, db: Session = Depends(get_db)):
    """获取单个通知"""
    db_notification = get_notification(db=db, notification_id=notification_id)
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="通知不存在")
    return db_notification


@router.get("/notifications", response_model=List[NotificationResponse])
async def read_notifications_route(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """获取通知列表"""
    return get_notifications(db=db, skip=skip, limit=limit)


@router.put("/notifications/{notification_id}", response_model=NotificationResponse)
async def update_notification_route(
    notification_id: str,
    notification_in: NotificationUpdate,
    db: Session = Depends(get_db),
):
    """更新通知"""
    db_notification = update_notification(
        db=db, notification_id=notification_id, notification_in=notification_in
    )
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="通知不存在")
    return db_notification


@router.delete(
    "/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_notification_route(
    notification_id: str, db: Session = Depends(get_db)
):
    """删除通知"""
    if not delete_notification(db=db, notification_id=notification_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="通知不存在")
    return None


@router.put(
    "/notifications/{notification_id}/status", response_model=NotificationResponse
)
async def update_notification_status_route(
    notification_id: str,
    status: NotificationStatus,
    db: Session = Depends(get_db),
):
    """根据 notification_id 修改通知已读/未读状态"""
    db_notification = update_notification_status(
        db=db, notification_id=notification_id, status=status
    )
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="通知不存在")
    return db_notification


@router.get("/notifications/users/{user_id}", response_model=List[NotificationResponse])
async def get_notifications_by_user_id_route(
    user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """根据 user_id 获取通知列表"""
    return get_notifications_by_user_id(db=db, user_id=user_id, skip=skip, limit=limit)

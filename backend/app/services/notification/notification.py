from sqlalchemy.orm import Session
from app.models.notifications import Notification, NotificationStatus
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)
from typing import List, Optional
import uuid


def create_notification(
    db: Session, notification_in: NotificationCreate
) -> Notification:
    """创建通知"""
    new_notification = Notification(
        notification_id=str(uuid.uuid4()),
        user_id=notification_in.user_id,
        task_id=notification_in.task_id,
        content=notification_in.content,
        ddl=notification_in.ddl,
        status=notification_in.status,
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def get_notification(db: Session, notification_id: str) -> Optional[Notification]:
    """获取单个通知"""
    return (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )


def get_notifications(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Notification]:
    """获取通知列表"""
    return db.query(Notification).offset(skip).limit(limit).all()


def update_notification(
    db: Session, notification_id: str, notification_in: NotificationUpdate
) -> Optional[Notification]:
    """更新通知"""
    db_notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )
    if not db_notification:
        return None

    if notification_in.content is not None:
        db_notification.content = notification_in.content
    if notification_in.ddl is not None:
        db_notification.ddl = notification_in.ddl
    if notification_in.status is not None:
        db_notification.status = notification_in.status

    db.commit()
    db.refresh(db_notification)
    return db_notification


def delete_notification(db: Session, notification_id: str) -> bool:
    """删除通知"""
    db_notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )
    if not db_notification:
        return False

    db.delete(db_notification)
    db.commit()
    return True


def update_notification_status(
    db: Session, notification_id: str, status: NotificationStatus
) -> Optional[Notification]:
    """根据 notification_id 修改通知已读/未读状态"""
    db_notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )
    if not db_notification:
        return None

    db_notification.status = status
    db.commit()
    db.refresh(db_notification)


def get_notifications_by_user_id(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
) -> List[Notification]:
    """根据 user_id 获取通知列表"""
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_notifications_by_task_id(
    db: Session, task_id: str, skip: int = 0, limit: int = 100
) -> List[Notification]:
    """根据 task_id 获取通知列表"""
    return (
        db.query(Notification)
        .filter(Notification.task_id == task_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

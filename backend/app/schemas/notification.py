from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.notifications import NotificationStatus


class NotificationCreate(BaseModel):
    task_id: str
    content: str
    ddl: datetime


class NotificationUpdate(BaseModel):
    content: Optional[str] = None
    ddl: Optional[datetime] = None
    status: Optional[NotificationStatus] = None


class NotificationResponse(BaseModel):
    notification_id: str
    user_id: str
    task_id: str
    content: str
    ddl: datetime
    status: NotificationStatus

    class Config:
        from_attributes = True

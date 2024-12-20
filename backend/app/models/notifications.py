from sqlalchemy import Column, String, TIMESTAMP, Text, Enum
from app.db.base import Base
import uuid
from enum import Enum as PyEnum


class NotificationStatus(PyEnum):
    READ = "read"
    UNREAD = "unread"


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(
        String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id = Column(String(50))
    task_id = Column(String(50))
    content = Column(Text, nullable=False)
    ddl = Column(TIMESTAMP, nullable=False)
    status = Column(
        Enum(NotificationStatus, name="notification_status"),
        nullable=False,
        default=NotificationStatus.UNREAD,
    )

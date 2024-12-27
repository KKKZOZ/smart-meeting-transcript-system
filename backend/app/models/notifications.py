from sqlalchemy import Column, String, TIMESTAMP, Text, Enum
from app.db.base import Base
import uuid
from enum import Enum as PyEnum


class NotificationStatus(PyEnum):
    READ = "READ"
    UNREAD = "UNREAD"


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

    def __str__(self):
        """
        返回一个对用户友好的字符串表示，用于 print() 函数。
        """
        return (
            f"Notification("
            f"notification_id={self.notification_id}, "
            f"user_id={self.user_id}, "
            f"task_id={self.task_id}, "
            f"status={self.status.value}, "  # 使用 .value 获取枚举值
            f"ddl={self.ddl.strftime('%Y-%m-%d %H:%M:%S') if self.ddl else None}, "  # 格式化时间
            f"content={'...'.join([self.content[:50]]) if self.content and len(self.content) > 50 else self.content}"
            f")"
        )

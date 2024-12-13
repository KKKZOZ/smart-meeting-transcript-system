from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text
from app.db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.user_id"))
    task_id = Column(String(50), ForeignKey("tasks.task_id"))
    content = Column(Text, nullable=False)
    ddl = Column(TIMESTAMP, nullable=False)
    status = Column(String(20), nullable=False)

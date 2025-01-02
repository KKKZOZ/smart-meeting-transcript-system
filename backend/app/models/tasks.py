from sqlalchemy import Column, String, ForeignKey, Text, TIMESTAMP
from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String(50), primary_key=True)
    meeting_id = Column(
        String(50), ForeignKey("meetings.meeting_id", ondelete="CASCADE")
    )
    description = Column(Text, nullable=False)
    inspector_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"))
    executor_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"))
    due_date = Column(TIMESTAMP, nullable=True)
    status = Column(String(20), nullable=False)

    def __str__(self):
        return (
            f"Task(task_id={self.task_id}, "
            f"meeting_id={self.meeting_id}, "
            f"description='{self.description}', "
            f"inspector_id={self.inspector_id}, "
            f"executor_id={self.executor_id}, "
            f"due_date={self.due_date}, "
            f"status={self.status})"
        )

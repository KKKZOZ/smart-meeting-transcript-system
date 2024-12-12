from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from app.db.base import Base


class Meeting(Base):
    __tablename__ = "Meetings"

    meeting_id = Column(String(50), primary_key=True)  # 修改为 VARCHAR(50)
    title = Column(String(200), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=True)
    language = Column(String(10), nullable=True)
    creator_id = Column(
        String(50), ForeignKey("users.user_id"), nullable=False
    )  # 修改为 VARCHAR(50)

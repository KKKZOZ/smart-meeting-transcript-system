from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text
from app.db.base import Base
from datetime import datetime


class Summary(Base):
    __tablename__ = "summaries"

    meeting_id = Column(String(50), ForeignKey("meetings.meeting_id"), primary_key=True)
    content = Column(Text, nullable=False)
    generated_at = Column(TIMESTAMP, nullable=False, default=datetime.now)

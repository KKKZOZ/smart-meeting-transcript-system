from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text, Boolean
from app.db.base import Base


class Transcription(Base):
    __tablename__ = "transcriptions"

    meeting_id = Column(String(50), ForeignKey("meetings.meeting_id"), primary_key=True)
    task_id = Column(String(50), nullable=True)
    task_status = Column(String(10), nullable=True)
    content = Column(Text, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    language = Column(String(10), nullable=True)
    # ischanged = Column(Boolean, default=False, nullable=False)
    ischanged = Column(Boolean, default=False)

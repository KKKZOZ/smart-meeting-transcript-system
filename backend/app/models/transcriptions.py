from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text
from app.db.base import Base


class Transcription(Base):
    __tablename__ = "transcriptions"

    meeting_id = Column(String(50), ForeignKey("meetings.meeting_id"), primary_key=True)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    language = Column(String(10), nullable=True)

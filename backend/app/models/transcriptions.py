from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text, Boolean, Integer
from app.db.base import Base


class Transcription(Base):
    __tablename__ = "transcriptions"

    meeting_id = Column(
        String(50),
        ForeignKey("meetings.meeting_id", ondelete="CASCADE"),
        primary_key=True,
    )
    task_id = Column(String(50), nullable=True)
    task_status = Column(String(10), nullable=True)
    content = Column(Text, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    language = Column(String(10), nullable=True)
    speaker_count = Column(Integer, default=0, nullable=True)
    ischanged = Column(Boolean, default=False, nullable=True)

    def __str__(self):
        return (
            f"Transcription(meeting_id={self.meeting_id}, task_id={self.task_id}, "
            f"task_status={self.task_status}, content={self.content[:50] if self.content else None}... , "
            f"timestamp={self.timestamp}, language={self.language}, "
            f"speaker_count={self.speaker_count}, ischanged={self.ischanged})"
        )

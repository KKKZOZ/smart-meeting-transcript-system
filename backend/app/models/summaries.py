from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text, Integer
from app.db.base import Base
from datetime import datetime


class Summary(Base):
    __tablename__ = "summaries"

    summary_id = Column(Integer, primary_key=True)
    meeting_id = Column(
        String(50),
        ForeignKey("meetings.meeting_id", ondelete="CASCADE")
    )
    content = Column(Text, nullable=False)
    summary_type = Column(
        String(21345),
        default="简要概述"  
    )
    generated_at = Column(TIMESTAMP, nullable=False, default=datetime.now)

    def __str__(self):
        return (
            f"Summary(\n"
            f"  summary_id={self.summary_id},\n"
            f"  meeting_id={self.meeting_id},\n"
            f"  content='{self.content}',\n"
            f"  summary_type={self.summary_type},\n"
            f"  generated_at={self.generated_at}\n"
            f")"
        )

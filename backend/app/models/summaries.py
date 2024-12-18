from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text, Enum
from app.db.base import Base
from datetime import datetime


class Summary(Base):
    __tablename__ = "summaries"

    meeting_id = Column(String(50), ForeignKey("meetings.meeting_id"), primary_key=True)
    content = Column(Text, nullable=False)
    SummaryType = Column(
        Enum(
            "简要概述",
            "决策事项",
            "正式(语言风格)",
            "非正式(语言风格)",
            name="summary_type",
        ),
        nullable=False,
    )
    language = Column(String(10), nullable=False)
    generated_at = Column(TIMESTAMP, nullable=False, default=datetime.now)

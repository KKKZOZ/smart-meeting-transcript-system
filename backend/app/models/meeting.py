from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from app.db.base import Base


class Meeting(Base):
    __tablename__ = "meetings"

    meeting_id = Column(String(50), primary_key=True)  # 修改为 VARCHAR(50)
    title = Column(String(200), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=True)
    language = Column(String(10), nullable=True)
    creator_id = Column(
        String(50), ForeignKey("users.user_id"), nullable=False
    )  # 修改为 VARCHAR(50)
    video_url = Column(String(200), nullable=True)


class MeetingParticipants(Base):
    __tablename__ = "meeting_participants"

    meeting_id = Column(String(50), ForeignKey("meetings.meeting_id"))
    participant_id = Column(String(50), ForeignKey("users.user_id"))
    # meeting_id和participant_id组合主键
    __table_args__ = (PrimaryKeyConstraint("meeting_id", "participant_id"),)

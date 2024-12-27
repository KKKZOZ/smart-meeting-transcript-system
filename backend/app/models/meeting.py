from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    ForeignKey,
    PrimaryKeyConstraint,
)
from app.db.base import Base


class Meeting(Base):
    __tablename__ = "meetings"

    meeting_id = Column(String(50), primary_key=True)  # 修改为 VARCHAR(50)
    title = Column(String(200), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=True)
    language = Column(String(10), nullable=True)
    creator_id = Column(
        String(50),
        ForeignKey("users.user_id", ondelete="CASCADE"),  # 添加级联删除
        nullable=False,
    )  # 修改为 VARCHAR(50)
    video_url = Column(String(200), nullable=True)

    def __str__(self):
        return (
            f"Meeting(\n"
            f"  meeting_id={self.meeting_id},\n"
            f"  title='{self.title}',\n"
            f"  start_time={self.start_time},\n"
            f"  end_time={self.end_time},\n"
            f"  language={self.language},\n"
            f"  creator_id={self.creator_id},\n"
            f"  video_url={self.video_url}\n"
            f")"
        )


class MeetingParticipants(Base):
    __tablename__ = "meeting_participants"

    meeting_id = Column(
        String(50), ForeignKey("meetings.meeting_id", ondelete="CASCADE")
    )
    participant_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"))
    # meeting_id和participant_id组合主键
    __table_args__ = (PrimaryKeyConstraint("meeting_id", "participant_id"),)

    def __str__(self):
        return (
            f"MeetingParticipants(\n"
            f"  meeting_id={self.meeting_id},\n"
            f"  participant_id={self.participant_id}\n"
            f")"
        )

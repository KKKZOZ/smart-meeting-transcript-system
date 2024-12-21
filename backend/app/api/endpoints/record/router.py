from typing import List
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting, MeetingParticipants
from app.models.user import User
from app.schemas.meeting import GetMeetingResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc


router = APIRouter()


@router.get("/getMeetings", response_model=List[GetMeetingResponse])
def get_meetings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有会议，按时间倒序排序
    """
    query = (
        db.query(Meeting)
        .outerjoin(User, Meeting.creator_id == User.user_id)
        .outerjoin(
            MeetingParticipants, Meeting.meeting_id == MeetingParticipants.meeting_id
        )
        .filter(
            (Meeting.creator_id == current_user.user_id)
            | (MeetingParticipants.participant_id == current_user.user_id)
        )
        .add_columns(User.username.label("creator_name"))
        .order_by(desc(Meeting.start_time))
        .distinct()
    )

    # 打印生成的SQL语句
    # print("Generated SQL:", str(query.statement))

    meetings = query.all()

    # 将 creator_name 添加到 Meeting 对象中
    for meeting, creator_name in meetings:
        setattr(meeting, "creator_name", creator_name)

    return [meeting for meeting, _ in meetings]

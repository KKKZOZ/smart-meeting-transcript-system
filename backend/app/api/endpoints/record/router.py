from typing import List
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting
from app.models.user import User
from app.schemas.meeting import MeetingResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc


router = APIRouter()


@router.get("/getMeetings", response_model=List[MeetingResponse])
def get_meetings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有会议，按时间倒序排序
    """
    meetings = (
        db.query(Meeting)
        .filter(Meeting.creator_id == current_user.user_id)
        .order_by(desc(Meeting.start_time))  # 假设 Meeting 模型中有 created_at 字段
        .all()
    )
    return meetings

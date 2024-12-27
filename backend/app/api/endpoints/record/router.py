from typing import List
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting, MeetingParticipants
from app.models.user import User
from app.schemas.meeting import (
    GetMeetingResponse,
    DeleteMeetingRequest,
    SearchMeetingRequest,
)
from fastapi import APIRouter, Depends, HTTPException
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


@router.delete("/deleteMeeting")
def delete_meeting(
    request: DeleteMeetingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除会议记录
    """
    # 查询会议是否存在
    meeting = db.query(Meeting).filter(Meeting.meeting_id == request.meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="会议不存在")

    # 验证当前用户是否为会议创建者
    if meeting.creator_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="只有会议创建者可以删除会议")

    try:
        # 直接删除会议记录，所有相关记录会自动被删除
        db.query(Meeting).filter(Meeting.meeting_id == request.meeting_id).delete()
        db.commit()

        return {"message": "会议删除成功"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除会议失败: {str(e)}")


@router.post("/searchMeeting", response_model=List[GetMeetingResponse])
def search_meeting(
    request: SearchMeetingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    搜索会议记录
    """
    query = (
        db.query(Meeting)
        .outerjoin(User, Meeting.creator_id == User.user_id)
        .outerjoin(
            MeetingParticipants, Meeting.meeting_id == MeetingParticipants.meeting_id
        )
        .filter(
            # 只能搜索自己创建的或参与的会议
            (Meeting.creator_id == current_user.user_id)
            | (MeetingParticipants.participant_id == current_user.user_id)
        )
        # 标题中包含搜索关键词
        .filter(Meeting.title.ilike(f"%{request.keyword}%"))
        .add_columns(User.username.label("creator_name"))
        .order_by(desc(Meeting.start_time))
        .distinct()
    )

    meetings = query.all()

    # 将 creator_name 添加到 Meeting 对象中
    for meeting, creator_name in meetings:
        setattr(meeting, "creator_name", creator_name)

    return [meeting for meeting, _ in meetings]

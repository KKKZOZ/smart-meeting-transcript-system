from typing import List
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting, MeetingParticipants
from app.models.user import User
from app.schemas.user import DeleteUserRequest
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

    # 先检查当前用户是否是root
    if not current_user.root:
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


@router.get("/getAllMeetings", response_model=List[GetMeetingResponse])
def get_all_meetings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取所有会议（仅root用户可用）
    """
    if not current_user.root:
        raise HTTPException(status_code=403, detail="只有管理员可以访问所有会议")

    query = (
        db.query(Meeting)
        .outerjoin(User, Meeting.creator_id == User.user_id)
        .add_columns(User.username.label("creator_name"))
        .order_by(desc(Meeting.start_time))
    )

    meetings = query.all()

    # 将 creator_name 添加到 Meeting 对象中
    for meeting, creator_name in meetings:
        setattr(meeting, "creator_name", creator_name)

    return [meeting for meeting, _ in meetings]


@router.post("/searchAllMeetings", response_model=List[GetMeetingResponse])
def search_all_meetings(
    request: SearchMeetingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    搜索所有会议（仅root用户可用）
    """
    if not current_user.root:
        raise HTTPException(status_code=403, detail="只有管理员可以搜索所有会议")

    query = (
        db.query(Meeting)
        .outerjoin(User, Meeting.creator_id == User.user_id)
        .filter(Meeting.title.ilike(f"%{request.keyword}%"))
        .add_columns(User.username.label("creator_name"))
        .order_by(desc(Meeting.start_time))
    )

    meetings = query.all()

    # 将 creator_name 添加到 Meeting 对象中
    for meeting, creator_name in meetings:
        setattr(meeting, "creator_name", creator_name)

    return [meeting for meeting, _ in meetings]


@router.get("/getAllUsers", response_model=List[dict])
def get_all_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取所有非root用户列表（仅root用户可用）
    """
    if not current_user.root:
        raise HTTPException(status_code=403, detail="只有管理员可以获取用户列表")

    users = db.query(User).filter(User.root == 0).order_by(User.username).all()
    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "enabled": user.enabled,
        }
        for user in users
    ]


@router.post("/searchAllUsers", response_model=List[dict])
def search_all_users(
    request: SearchMeetingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    搜索非root用户（仅root用户可用）
    """
    if not current_user.root:
        raise HTTPException(status_code=403, detail="只有管理员可以搜索用户")

    users = (
        db.query(User)
        .filter(User.root == 0)
        .filter(
            (User.username.ilike(f"%{request.keyword}%"))
            | (User.nickname.ilike(f"%{request.keyword}%"))
            | (User.email.ilike(f"%{request.keyword}%"))
        )
        .order_by(User.username)
        .all()
    )

    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "enabled": user.enabled,
        }
        for user in users
    ]


@router.delete("/deleteUser")
def delete_user(
    request: DeleteUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除用户（仅root用户可以删除非root用户）
    """
    if not current_user.root:
        raise HTTPException(status_code=403, detail="只有管理员可以删除用户")

    # 查询要删除的用户
    user_to_delete = db.query(User).filter(User.user_id == request.user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 检查要删除的用户是否为root用户
    if user_to_delete.root:
        raise HTTPException(status_code=403, detail="不能删除管理员用户")

    try:
        db.delete(user_to_delete)
        db.commit()
        return {"message": "用户删除成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除用户失败: {str(e)}")

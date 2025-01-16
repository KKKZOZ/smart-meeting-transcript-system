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
from datetime import datetime, timedelta


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


@router.get("/overview", response_model=dict)
def get_meeting_overview(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取用户的会议统计概览
    """
    print("get_meeting_overview")
    # 获取用户创建的会议数量
    created_meetings_count = (
        db.query(Meeting).filter(Meeting.creator_id == current_user.user_id).count()
    )

    # 获取用户参与的会议数量（不包括自己创建的）
    participated_meetings_count = (
        db.query(Meeting)
        .join(MeetingParticipants, Meeting.meeting_id == MeetingParticipants.meeting_id)
        .filter(MeetingParticipants.participant_id == current_user.user_id)
        .count()
    )

    # 获取合作的用户数量（包括创建的会议的参与者和参与的会议的创建者与其他参与者）
    collaborated_users = set()

    # 获取用户参与的所有会议ID
    user_meeting_ids = (
        db.query(MeetingParticipants.meeting_id)
        .filter(MeetingParticipants.participant_id == current_user.user_id)
        .all()
    )

    print(user_meeting_ids)
    # 获取这些会议中的所有参与者
    if user_meeting_ids:
        meeting_ids = [meeting_id[0] for meeting_id in user_meeting_ids]
        other_participants = (
            db.query(MeetingParticipants.participant_id)
            .filter(
                MeetingParticipants.meeting_id.in_(meeting_ids),
                MeetingParticipants.participant_id != current_user.user_id,
            )
            .all()
        )
        print(other_participants)
        for participant in other_participants:
            collaborated_users.add(participant[0])

    # 计算会议总时长（分钟）
    total_duration = 0.0
    # 初始化最近9个月的数据
    current_date = datetime.now()
    nine_months_ago = current_date - timedelta(days=270)
    monthly_data = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 初始化9个月的数据数组

    all_meetings = (
        db.query(Meeting)
        .filter(
            (Meeting.creator_id == current_user.user_id)
            | Meeting.meeting_id.in_(
                db.query(MeetingParticipants.meeting_id).filter(
                    MeetingParticipants.participant_id == current_user.user_id
                )
            )
        )
        .all()
    )

    for meeting in all_meetings:
        if meeting.start_time and meeting.end_time:
            duration = (meeting.end_time - meeting.start_time).total_seconds() / 60
            if duration < 0:
                duration = 0
            total_duration += duration

            # 如果会议在最近9个月内，添加到月度数据中
            if meeting.start_time >= nine_months_ago:
                # 计算会议月份与当前月份的差距
                months_diff = (current_date.year - meeting.start_time.year) * 12 + (
                    current_date.month - meeting.start_time.month
                )
                if months_diff < 9:
                    monthly_data[8 - months_diff] = round(
                        monthly_data[8 - months_diff] + duration, 2
                    )

    print("monthly_data", monthly_data)
    return {
        "created_meetings": created_meetings_count,
        "participated_meetings": participated_meetings_count,
        "collaborators": len(collaborated_users),
        "total_duration": total_duration,
        "monthly_data": monthly_data,
    }

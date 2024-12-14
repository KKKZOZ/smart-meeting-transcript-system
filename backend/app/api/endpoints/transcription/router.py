from uuid import uuid4

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting, MeetingParticipants
from app.schemas.meeting import MeetingCreate, MeetingResponse, ParticipantResponse
from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.post("/meetings", response_model=MeetingResponse)
def create_meeting(
    meeting_in: MeetingCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    创建会议记录
    """
    user_id = user.user_id
    meeting_id = uuid4()  # 生成唯一的会议 ID
    new_meeting = Meeting(
        meeting_id=meeting_id,
        title=meeting_in.title,
        start_time=meeting_in.start_time,
        end_time=meeting_in.end_time,
        language=meeting_in.language,
        creator_id=user_id,  # 使用从请求头提取的用户ID
    )
    # print(f"Decoded user_id: {user_id}")
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    # 将每个参与者与会议结合并插入到 meeting_participants 表中
    for participant_id in meeting_in.participants:
        meeting_participant = MeetingParticipants(
            meeting_id=meeting_id, participant_id=participant_id
        )
        db.add(meeting_participant)

    db.commit()  # 提交更改，保存到数据库

    return new_meeting


@router.get("/getUsers", response_model=List[ParticipantResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    获取所有用户
    """
    users = db.query(
        User.user_id.label("participant_id"), User.username.label("participant_name")
    ).all()
    return users


# 创建会议：用户id，会议名称，起止时间，会议语言，用户成员；return t/f
# 音频上传/修改音频/录音：
# 转文字：通过调用其他非路由函数完成
# 修改人员：键值对

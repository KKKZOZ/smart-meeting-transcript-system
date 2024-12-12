from uuid import uuid4

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate, MeetingResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/meetings", response_model=MeetingResponse)
def create_meeting(
    meeting_in: MeetingCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    创建会议记录
     user_id: str = Depends(get_current_user)
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

    return new_meeting


# 创建会议：用户id，会议名称，起止时间，会议语言，用户成员；return t/f
# 音频上传/修改音频/录音：
# 转文字：通过调用其他非路由函数完成
# 修改人员：键值对

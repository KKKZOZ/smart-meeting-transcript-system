from datetime import datetime

from pydantic import BaseModel


class MeetingCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    language: str


class MeetingResponse(BaseModel):
    meeting_id: str  # 修改为 str，因为数据库中的 meeting_id 是 VARCHAR(50)
    title: str
    start_time: datetime
    end_time: datetime
    language: str
    creator_id: str  # 修改为 str，因为数据库中的 creator_id 是 VARCHAR(50)

    class Config:
        orm_mode = True  # 支持从 ORM 模型直接转为 Pydantic 模型

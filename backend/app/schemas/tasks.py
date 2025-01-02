from datetime import datetime
from pydantic import BaseModel


class MeetingsToExtract(BaseModel):
    meeting_id: str
    title: str
    content: str
    start_time: datetime
    creator_name: str

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    id: str
    name: str
    nickname: str

    class Config:
        orm_mode = True


class MeetingId(BaseModel):
    meeting_id: str


class TasksToCreate(BaseModel):
    inspector: str
    meeting_id: str
    tasks: list


class TasksToExecuteResponse(BaseModel):
    task_id: str
    meeting_id: str
    meeting_title: str
    description: str
    inspector_id: str
    inspector_name: str
    inspector_nickname: str
    due_date: datetime
    status: str

    class Config:
        orm_mode = True


class TasksToReviewResponse(BaseModel):
    task_id: str
    meeting_id: str
    meeting_title: str
    description: str
    executor_id: str
    executor_name: str
    executor_nickname: str
    due_date: datetime
    status: str

    class Config:
        orm_mode = True


class TasksToHandle(BaseModel):
    task_id: str

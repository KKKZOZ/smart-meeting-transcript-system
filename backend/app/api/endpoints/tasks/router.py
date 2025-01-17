from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.tasks import (
    MeetingsToExtract,
    UserInfo,
    MeetingId,
    TasksToCreate,
    TasksToExecuteResponse,
    TasksToReviewResponse,
    TasksToHandle,
)
import app.services.tasks.extraction as extraction

router = APIRouter()


@router.post("/meetings-to-extract", response_model=List[MeetingsToExtract])
async def meetings_to_extract(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取当前用户已转录的所有会议，按时间倒序排序
    """
    meetings = extraction.get_transcripted_meetings(db, current_user)

    return meetings


@router.post("/get-user-info", response_model=List[UserInfo])
async def get_user_info(db: Session = Depends(get_db)):
    """
    获取所有用户信息
    """
    return extraction.get_user_information(db)


@router.post("/llm-extraction")
async def extract_tasks(meeting_id: MeetingId, db: Session = Depends(get_db)):
    """
    提取任务项
    """
    # 根据会议id查表，获取内容和时间
    query_result = extraction.get_meeting_info(meeting_id, db)
    content = query_result[0][0]
    time = str(query_result[0][1])

    # 提取待办事项
    result = extraction.llm_extract(content, time)

    if result is None:
        return {"message": "fail"}
    else:
        return {"message": "success", "data": result}


@router.post("/create-tasks")
async def create_tasks(tasks_info: TasksToCreate, db: Session = Depends(get_db)):
    """
    创建任务项
    """
    if extraction.create_tasks(tasks_info, db):
        return {"message": "success"}
    else:
        return {"message": "fail"}


@router.post("/get-tasks-to-review", response_model=List[TasksToReviewResponse])
async def get_tasks_to_review(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取要检查的任务项
    """
    return extraction.get_tasks_to_review(db, current_user)


@router.post("/get-tasks-to-execute", response_model=List[TasksToExecuteResponse])
async def get_tasks_to_execute(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取要执行的任务项
    """
    return extraction.get_tasks_to_execute(db, current_user)


@router.post("/submit-tasks")
async def submit_tasks(tasks_info: TasksToHandle, db: Session = Depends(get_db)):
    """
    提交任务项
    """
    if not extraction.submit_tasks(tasks_info, db):
        return {"message": "fail"}
    else:
        return {"message": "success"}


@router.post("/remind-tasks")
async def remind_tasks(tasks_info: TasksToHandle, db: Session = Depends(get_db)):
    """
    提醒提交任务项
    """
    note = extraction.remind_tasks(tasks_info, db)

    if not note:
        return {"message": "fail"}
    else:
        return {"message": "success"}

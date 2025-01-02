from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import APIRouter, Depends
from uuid import uuid4
from datetime import datetime
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.meeting import Meeting, MeetingParticipants
from app.models.user import User
from app.models.transcriptions import Transcription
from app.models.tasks import Task
from app.schemas.tasks import (
    MeetingsToExtract,
    UserInfo,
    MeetingId,
    TasksToCreate,
    TasksToExecuteResponse,
    TasksToReviewResponse,
    TasksToHandle,
)
from app.schemas.notification import NotificationCreate
from app.services.tasks.extraction import llm_extract
from app.services.notification.notification import create_notification

router = APIRouter()


@router.post("/meetings-to-extract", response_model=List[MeetingsToExtract])
async def meetings_to_extract(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取当前用户已转录的所有会议，按时间倒序排序
    """
    query = (
        db.query(
            Meeting.meeting_id,
            Meeting.title,
            Transcription.content,
            Meeting.start_time,
            User.nickname.label("creator_name"),
        )
        .join(User, Meeting.creator_id == User.user_id)
        .join(MeetingParticipants, Meeting.meeting_id == MeetingParticipants.meeting_id)
        .join(Transcription, Meeting.meeting_id == Transcription.meeting_id)
        .filter(
            (Meeting.creator_id == current_user.user_id)
            | (MeetingParticipants.participant_id == current_user.user_id)
        )
        .order_by(desc(Meeting.start_time))
        .distinct()
    )

    meetings = query.all()

    return meetings


@router.post("/get-user-info", response_model=List[UserInfo])
async def get_user_info(db: Session = Depends(get_db)):
    """
    获取用户信息
    """
    query = db.query(
        User.user_id.label("id"), User.username.label("name"), User.nickname
    )

    return query.all()


@router.post("/llm-extraction")
async def extract_tasks(meeting_id: MeetingId, db: Session = Depends(get_db)):
    """
    提取任务项
    """
    # 根据会议id查表，获取内容和时间
    query_result = (
        db.query(Transcription.content, Transcription.timestamp)
        .filter(Transcription.meeting_id == meeting_id.meeting_id)
        .all()
    )
    content = query_result[0][0]
    time = str(query_result[0][1])

    # 提取待办事项
    result = llm_extract(content, time)

    if result is None:
        return {"message": "fail"}
    else:
        return {"message": "success", "data": result}


@router.post("/create-tasks")
async def create_tasks(tasks_info: TasksToCreate, db: Session = Depends(get_db)):
    """
    创建任务项
    """
    try:
        for task in tasks_info.tasks:
            new_task = Task(
                task_id=uuid4(),
                meeting_id=tasks_info.meeting_id,
                description=task["content"],
                inspector_id=tasks_info.inspector,
                executor_id=task["executor"],
                due_date=datetime.fromisoformat(task["dueDate"]),
                status="待处理",
            )
            db.add(new_task)
        db.commit()
        return {"message": "success"}
    except Exception:
        return {"message": "fail"}


@router.post("/get-tasks-to-review", response_model=List[TasksToReviewResponse])
async def get_tasks_to_review(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取要检查的任务项
    """
    query = (
        db.query(
            Task.task_id,
            Meeting.meeting_id,
            Meeting.title.label("meeting_title"),
            Task.description,
            User.user_id.label("executor_id"),
            User.username.label("executor_name"),
            User.nickname.label("executor_nickname"),
            Task.due_date,
            Task.status,
        )
        .join(Meeting, Task.meeting_id == Meeting.meeting_id)
        .join(User, Task.executor_id == User.user_id)
        .filter(Task.inspector_id == current_user.user_id)
    )
    return query.all()


@router.post("/get-tasks-to-execute", response_model=List[TasksToExecuteResponse])
async def get_tasks_to_execute(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    获取要执行的任务项
    """
    query = (
        db.query(
            Task.task_id,
            Meeting.meeting_id,
            Meeting.title.label("meeting_title"),
            Task.description,
            User.user_id.label("inspector_id"),
            User.username.label("inspector_name"),
            User.nickname.label("inspector_nickname"),
            Task.due_date,
            Task.status,
        )
        .join(Meeting, Task.meeting_id == Meeting.meeting_id)
        .join(User, Task.inspector_id == User.user_id)
        .filter(Task.executor_id == current_user.user_id)
    )
    return query.all()


@router.post("/submit-tasks")
async def submit_tasks(tasks_info: TasksToHandle, db: Session = Depends(get_db)):
    """
    提交任务项
    """
    submit = db.query(Task).filter(Task.task_id == tasks_info.task_id).first()
    submit.status = "已完成"

    db.commit()
    db.refresh(submit)

    # notification

    if not submit:
        return {"message": "fail"}
    else:
        return {"message": "success"}


@router.post("/remind-tasks")
async def remind_tasks(tasks_info: TasksToHandle, db: Session = Depends(get_db)):
    """
    提醒提交任务项
    """
    # 获取待办事项信息
    details = (
        db.query(Task.description, Task.due_date, Task.executor_id, User.nickname)
        .join(User, Task.inspector_id == User.user_id)
        .filter(Task.task_id == tasks_info.task_id)
        .first()
    )
    # 创建通知
    note = create_notification(
        db,
        NotificationCreate(
            task_id=tasks_info.task_id,
            content=f'{details[3]}提醒您尽快处理任务"{details[0]}"',
            ddl=details[1],
        ),
        details[2],
    )

    if not note:
        return {"message": "fail"}
    else:
        return {"message": "success"}

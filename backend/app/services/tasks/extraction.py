import json
import re
from app.core.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import uuid4
from datetime import datetime
from app.models.meeting import Meeting, MeetingParticipants
from app.models.user import User
from app.models.transcriptions import Transcription
from app.models.tasks import Task
from app.schemas.tasks import (
    MeetingId,
    TasksToCreate,
    TasksToHandle,
)
from app.schemas.notification import NotificationCreate
from app.services.notification.notification import create_notification


def extract_and_check_task_json(response: str) -> str:
    """
    从LLM的响应中提取待办事项的JSON，并检查是否合法，失败时返回None
    合法则增加searchExecutor: ''用于对应前端的功能
    """
    # 使用正则表达式提取JSON列表
    json_pattern = r"\[.*?\]"  # 匹配JSON列表的正则表达式
    match = re.search(json_pattern, response, re.DOTALL)

    if not match:
        return None

    # 提取到的JSON列表部分
    json_str = match.group(0)

    try:
        # 解析JSON字符串
        json_list = json.loads(json_str)

        # 检查每个对象是否只包含 "content", "executor", "dueDate" 这三个键
        for obj in json_list:
            if not isinstance(obj, dict):
                return None

            # 获取当前对象的所有键
            keys = set(obj.keys())
            expected_keys = {"content", "executor", "dueDate"}

            # 检查是否完全匹配
            if keys != expected_keys:
                return None

            # 增加searchExecutor: ''用于对应前端的功能
            obj["searchExecutor"] = ""

        return json_list

    except json.JSONDecodeError:
        return None


def llm_extract(records: str, meeting_time: str) -> str:
    """
    从会议记录中提取任务项
    """
    # 获取API信息
    api_key = settings.OPENAI_API_KEY
    base_url = settings.OPENAI_API_BASE

    # 定义Prompt
    template = """
    请从<begin>、<end>间的会议记录中提取出所有任务项，要求如下：
    1.  用JSON列表的格式输出任务项
    2.  JSON列表的每一项的形式为{json_type}
    3.  JSON中键对应的值使用的语言与会议记录相同
    4.  任务项中的某部分在会议记录中未提及用空字符串""填充
    5.  会议举行的时间为{meeting_time}
    <begin>
    {content}
    <end>
    """
    json_type = """
        {
            "content": "任务描述",
            "executor": "任务负责人",
            "dueDate": "yyyy-MM-dd HH:MM"
        }
    """
    prompt = PromptTemplate.from_template(template).format(
        json_type=json_type, meeting_time=meeting_time, content=records
    )
    # 创建OpenAI实例
    llm = ChatOpenAI(api_key=api_key, base_url=base_url)

    # 执行模型调用
    response = llm.invoke(prompt)

    # 提取JSON并检查，失败重试一次
    res_json = extract_and_check_task_json(response.content)
    if res_json is None:
        response = llm.invoke(prompt)
        res_json = extract_and_check_task_json(response.content)
    return res_json


def get_transcripted_meetings(db: Session, current_user: User):
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

    return query.all()


def get_user_information(db: Session):
    """
    获取所有用户信息
    """
    query = db.query(
        User.user_id.label("id"), User.username.label("name"), User.nickname
    )

    return query.all()


def get_meeting_info(meeting_id: MeetingId, db: Session):
    """
    获取会议信息
    """
    query = db.query(Transcription.content, Transcription.timestamp).filter(
        Transcription.meeting_id == meeting_id.meeting_id
    )

    return query.all()


def create_tasks(tasks_info: TasksToCreate, db: Session):
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
        return True
    except Exception:
        return False


def get_tasks_to_review(db: Session, current_user: User):
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


def get_tasks_to_execute(db: Session, current_user: User):
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


def submit_tasks(tasks_info: TasksToHandle, db: Session):
    """
    提交任务项
    """
    submit = db.query(Task).filter(Task.task_id == tasks_info.task_id).first()
    submit.status = "已完成"

    db.commit()
    db.refresh(submit)

    if not submit:
        return False
    else:
        # 获取待办事项信息
        details = (
            db.query(Task.description, Task.due_date, Task.inspector_id, User.nickname)
            .join(User, Task.executor_id == User.user_id)
            .filter(Task.task_id == tasks_info.task_id)
            .first()
        )
        # 创建通知
        note = create_notification(
            db,
            NotificationCreate(
                task_id=tasks_info.task_id,
                content=f'{details[3]}的任务"{details[0]}"已完成',
                ddl=details[1],
            ),
            details[2],
        )

        if not note:
            return False
        else:
            return True


def remind_tasks(tasks_info: TasksToHandle, db: Session):
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

    return note

import os
import json
import threading
from typing import List
from uuid import uuid4
from datetime import datetime
from app.core.security import get_current_user
from app.services.transcription import (
    upload,
    translate,
    create_task,
    poll_task_status,
    splicing,
    splicing_second,
)
from app.db.session import get_db
from app.models.meeting import Meeting, MeetingParticipants
from app.models.transcriptions import Transcription
from app.models.user import User
from app.schemas.meeting import MeetingCreate, MeetingResponse, ParticipantResponse
from fastapi import APIRouter, Depends, UploadFile, File, Form
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
        video_url="",
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

    meeting_response = MeetingResponse(
        meeting_id=new_meeting.meeting_id,
        title=new_meeting.title,
        start_time=new_meeting.start_time,
        end_time=new_meeting.end_time,
        language=new_meeting.language,
        creator_id=new_meeting.creator_id,
        creator_name="",  # 添加创建者名称
        video_url="",
    )
    return meeting_response


@router.get("/getUsers", response_model=List[ParticipantResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    获取所有用户
    """
    users = db.query(
        User.user_id.label("participant_id"), User.username.label("participant_name")
    ).all()
    return users


@router.get("/getParticipants", response_model=List[ParticipantResponse])
def get_participants(meeting_id: str, db: Session = Depends(get_db)):
    """
    获取该会议所有参与者
    """
    participants = (
        db.query(
            User.user_id.label("participant_id"),
            User.username.label("participant_name"),
        )
        .join(MeetingParticipants, MeetingParticipants.participant_id == User.user_id)
        .filter(MeetingParticipants.meeting_id == meeting_id)
        .all()
    )

    return participants


@router.get("/getTransStatus")
def get_tran_status(meeting_id: str, db: Session = Depends(get_db)):
    """
    获取对应会议id的转译内容
    返回：
        0 - 转录内容不存在或 task_status 为 null
        1 - 转录内容正在进行中（task_status = 'ongoing'）
        2 - 转录内容已完成（task_status = 'finished'）
    """
    # 查询转录内容
    transcription = (
        db.query(Transcription).filter(Transcription.meeting_id == meeting_id).first()
    )
    status = -1

    if not transcription:
        status = -1  # 如果转录内容不存在，返回 -1
        ischanged = False
        content = ""
        speaker_count = 0
    else:
        ischanged = transcription.ischanged
        speaker_count = transcription.speaker_count
        if transcription.task_status is None:
            status = 0  # 如果没有找到转录内容或 task_status 为 null，返回 0
        if transcription.task_status == "ONGOING":
            status = 1
        if transcription.task_status == "COMPLETED":
            status = 2
        if transcription.content is None:
            content = ""
        else:
            content = transcription.content
    # 查询视频URL
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    return {
        "status": status,
        "content": content,
        "video_url": meeting.video_url,
        "ischanged": ischanged,
        "speaker_count": speaker_count,
    }


@router.post("/upload", response_model=MeetingResponse)
async def upload_file(
    meeting_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    接收前端传递的文件并保存到本地。
    """
    uploaded_files = "./app/audio/"
    if not os.path.exists(uploaded_files):
        os.mkdir(uploaded_files)
    with open(f"{uploaded_files}/{file.filename}", "wb") as f:
        f.write(await file.read())

    result = upload(f"./app/audio/{file.filename}")
    print(f"上传成功: {result[0]}, 权限修改成功: {result[1]}, 地址为: {result[2]}")

    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()

    meeting.video_url = result[2]

    new_transcription = Transcription(
        meeting_id=meeting_id,
        timestamp=datetime.utcnow(),
        language=meeting.language,
    )

    db.add(new_transcription)
    db.commit()

    meeting_response = MeetingResponse(
        meeting_id=meeting.meeting_id,
        title=meeting.title,
        start_time=meeting.start_time,
        end_time=meeting.end_time,
        language=meeting.language,
        creator_id=meeting.creator_id,
        creator_name="",  # 添加创建者名称
        video_url=meeting.video_url,
    )
    return meeting_response


@router.post("/translate")
async def get_translate(
    meeting_id: str = Form(...),
    to_language: str = Form(...),
    db: Session = Depends(get_db),
):
    # 1. 根据 meeting_id 查询 transcriptions 表
    transcription = (
        db.query(Transcription).filter(Transcription.meeting_id == meeting_id).first()
    )

    # 2. 如果没有找到对应的记录，返回错误消息
    if not transcription or not transcription.content:
        return {"error": "Content not found for the given meeting_id"}

    # 3. 获取 content 字段
    content = transcription.content
    language = transcription.language
    # 4. 调用 translate 函数进行翻译
    translated_text = translate(content, language, to_language)

    # 5. 返回翻译后的文本
    return {"original": content, "translated": translated_text}


@router.post("/transcript")
async def transcript(meeting_id: str = Form(...), db: Session = Depends(get_db)):
    # 1. 查询数据库获得video_url
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        return {"error": "Meeting not found"}

    video_url = meeting.video_url

    # 2. 调用create_task，获取返回值并提取taskId
    before_response = create_task(video_url)
    r = json.loads(before_response)
    task_id = r.get("Data", {}).get("TaskId", "UNKNOWN")

    # 3. 保存task_id和更新task_status为ONGOING
    transcription = (
        db.query(Transcription).filter(Transcription.meeting_id == meeting_id).first()
    )
    if transcription:
        transcription.task_id = task_id
        transcription.task_status = "ONGOING"
        db.commit()

    # 4. 创建线程，执行poll_task_status
    def task_thread():
        # 在新线程中获取一个新的数据库会话
        thread_db = Session(bind=db.get_bind())

        # 轮询任务状态
        poll_response = poll_task_status(task_id)

        # 5. 调用splicing处理数据
        content, speaker_count = splicing(poll_response)

        # 6. 保存splicing返回的内容
        transcription = (
            thread_db.query(Transcription)
            .filter(Transcription.meeting_id == meeting_id)
            .first()
        )
        if transcription:
            transcription.content = content
            transcription.task_status = "COMPLETED"
            transcription.speaker_count = speaker_count
            thread_db.commit()
        thread_db.close()

    # 启动新线程执行任务
    threading.Thread(target=task_thread, daemon=True).start()

    return {"message": "Task started successfully", "task_id": task_id}


@router.post("/setSpeaker")
async def set_speaker(
    meeting_id: str = Form(...),
    speakers: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        # 1. 根据 meeting_id 找到 task_id
        transcription = (
            db.query(Transcription)
            .filter(Transcription.meeting_id == meeting_id)
            .first()
        )

        task_id = transcription.task_id
        print(speakers)
        # 2. 调用 poll_task_status 来获取任务状态/转录内容
        poll_response = poll_task_status(
            task_id, 1
        )  # 假设 poll_task_status 函数已经定义

        # 3. 使用 splicingNew 函数处理转录数据
        content = splicing_second(
            poll_response, speakers
        )  # 假设 splicingNew 函数已经定义

        # 4. 将处理后的 content 保存到会议的 content 字段
        transcription.content = content
        transcription.ischanged = True
        db.commit()

        return {"message": "Speaker content updated successfully", "content": content}

    except Exception as e:
        print(e)

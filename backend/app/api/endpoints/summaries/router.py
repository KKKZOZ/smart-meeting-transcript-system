from app.services.summary.summarize import summary_generate
from app.db.session import get_db
from app.models.meeting import Meeting
from app.models.summaries import Summary
from app.models.transcriptions import Transcription
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

router = APIRouter()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@router.get("/getMeetingData")
def get_meeting_data(db: Session = Depends(get_db)):
    """
    获取所有用户
    """
    meetings = db.query(
        # User.user_id.label("participant_id"),
        # User.username.label("participant_name"),
        Transcription.meeting_id,
        Transcription.timestamp,
        Transcription.content,
    ).all()
    meetingid_list = []
    title_list = []
    content_list = []
    timestamp_list = []
    for meeting in meetings:
        meetingid_list.append(meeting[0])
        timestamp_list.append(meeting[1])
        content_list.append(meeting[2])

    for meetingid in meetingid_list:
        title = db.query(Meeting.title).filter(Meeting.meeting_id == meetingid).first()
        title_list.append(title[0])

    logger.info(title_list)
    return {
        "title": title_list,
        "content": content_list,
        "timestamp": timestamp_list,
        "meeting_id": meetingid_list,
    }


@router.get("/genSummary")
def get_summary(type, content, db: Session = Depends(get_db)):
    logger.info("_______________________________")
    # decoded_para = unquote(para)
    # content, summary_type = para.split("##@##")
    # logger.info(para)
    logger.info(type)
    logger.info(content)
    # logger.info(summary_type)
    logger.info("_______________________________")
    summary = summary_generate(content, type)
    logger.info(summary)

    return str(summary)


@router.get("/confirmSummary")
def confirm_summary(content, meeting_id, type, db: Session = Depends(get_db)):
    # 使用db.insert将content，meeting_id，type插入summaries
    logger.info("_______________________________!!!!!!!!!!!!!!!")
    logger.info(content)
    logger.info(meeting_id)
    logger.info(type)
    new_summary = Summary(meeting_id=meeting_id, content=content, summary_type=type)
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return "success"


@router.get("/checkhistory")
def check_history(meeting_id, db: Session = Depends(get_db)):
    logger.info("!!!!!!!!!!!______________________")
    summaries = (
        db.query(
            Summary.content,
            Summary.summary_type,
            Summary.generated_at,
        )
        .filter(Summary.meeting_id == meeting_id)
        .all()
    )
    content_list = []
    type_list = []
    time_list = []
    for summary in summaries:
        content_list.append(summary[0])
        type_list.append(summary[1])
        time_list.append(summary[2])
    logger.info("!!!!!!!!!!!______________________")
    logger.info(content_list)
    logger.info(type_list)
    logger.info(time_list)
    return {"content": content_list, "type": type_list, "time": time_list}


@router.get("/deletehistory")
def delete_history(meeting_id, content, db: Session = Depends(get_db)):
    summary = db.query(Summary).filter(Summary.content == content).first()
    db.delete(summary)
    db.commit()
    summaries = (
        db.query(
            Summary.content,
            Summary.summary_type,
            Summary.generated_at,
        )
        .filter(Summary.meeting_id == meeting_id)
        .all()
    )
    content_list = []
    type_list = []
    time_list = []
    for summary in summaries:
        content_list.append(summary[0])
        type_list.append(summary[1])
        time_list.append(summary[2])
    return {"content": content_list, "type": type_list, "time": time_list}


@router.get("/searchquery")
def search_query(s_query, db: Session = Depends(get_db)):
    """
    获取所有用户
    """

    logger.info("_______________________________")
    logger.info(s_query)
    meetings = db.query(
        Transcription.meeting_id,
        Transcription.content,
        Transcription.timestamp,
    ).all()
    meetingid_list = []
    title_list = []
    content_list = []
    timestamp_list = []
    for meeting in meetings:
        meetingid_list.append(meeting[0])
        content_list.append(meeting[1])
        timestamp_list.append(meeting[2])
    for meetingid in meetingid_list:
        title = db.query(Meeting.title).filter(Meeting.meeting_id == meetingid).first()
        title_list.append(title[0])

    new_title_list = []
    new_content_list = []
    new_timestamp_list = []
    new_meetingid_list = []
    for i in range(len(title_list)):
        if s_query in title_list[i] or s_query in content_list[i]:
            new_title_list.append(title_list[i])
            new_content_list.append(content_list[i])
            new_timestamp_list.append(timestamp_list[i])
            new_meetingid_list.append(meetingid_list[i])

    return {
        "title": new_title_list,
        "content": new_content_list,
        "timestamp": new_timestamp_list,
        "meeting_id": new_meetingid_list,
    }

from datetime import datetime
from typing import List
from pydantic import BaseModel


class MeetingCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    language: str
    participants: List[str]


class MeetingResponse(BaseModel):
    meeting_id: str
    title: str
    start_time: datetime
    end_time: datetime
    language: str
    creator_id: str
    creator_name: str
    video_url: str

    class Config:
        orm_mode = True


class GetMeetingResponse(MeetingResponse):
    creator_name: str


class ParticipantResponse(BaseModel):
    participant_id: str
    participant_name: str

    class Config:
        orm_mode = True


class DeleteMeetingRequest(BaseModel):
    meeting_id: str


class SearchMeetingRequest(BaseModel):
    keyword: str

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    meeting_id: str
    task_id: Optional[str] = None  # 可以为 None
    task_status: Optional[str] = None  # 可以为 None
    content: Optional[str] = None  # 可以为 None
    timestamp: datetime
    language: Optional[str] = None  # 可以为 None

    class Config:
        orm_mode = True  # 支持从 ORM 模型直接转为 Pydantic 模型

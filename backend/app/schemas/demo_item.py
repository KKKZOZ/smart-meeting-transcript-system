from pydantic import BaseModel
from typing import Optional


class DemoItemCreate(BaseModel):
    id: int
    value: str = ""


class DemoItemUpdate(BaseModel):
    value: Optional[str] = None


class DemoItemResponse(BaseModel):
    id: int
    value: str

    class Config:
        from_attributes = True

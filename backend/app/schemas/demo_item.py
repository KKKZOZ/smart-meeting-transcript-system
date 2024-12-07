from pydantic import BaseModel
from typing import Optional


class DemoItemCreate(BaseModel):
    id: int
    value: int = 0


class DemoItemUpdate(BaseModel):
    value: Optional[int] = None


class DemoItemResponse(BaseModel):
    id: int
    value: int

    class Config:
        from_attributes = True

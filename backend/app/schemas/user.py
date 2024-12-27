from pydantic import BaseModel
from typing import Optional
import re


class UserBase(BaseModel):
    """用户基础模型"""

    username: str
    nickname: str
    email: Optional[str] = None

    @classmethod
    def validate_email(cls, v):
        if v is None:
            return v
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", v):
            raise ValueError("无效的邮箱格式")
        return v


class UserCreate(UserBase):
    """用户创建模型"""

    password: str


class User(UserBase):
    """用户信息模型"""

    user_id: str

    class Config:
        # 允许从ORM模型创建
        from_attributes = True


class Token(BaseModel):
    """令牌模型"""

    access_token: str
    token_type: str


class UserUpdate(UserBase):
    """用户信息更新模型"""

    password: Optional[str] = None
    notification_type: Optional[bool] = None
    frequency: Optional[str] = None

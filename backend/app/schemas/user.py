from pydantic import BaseModel, field_validator, Field
from typing import Optional
import re


class UserBase(BaseModel):
    """用户基础模型"""

    username: str = Field(..., min_length=3, max_length=20)
    email: str
    nickname: str = Field(..., min_length=2, max_length=20)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", v):
            raise ValueError("用户名只能包含字母、数字、下划线和连字符，长度在3-20之间")
        return v

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, v):
        if not re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9_-]{2,20}$", v):
            raise ValueError(
                "昵称可以包含中文、字母、数字、下划线和连字符，长度在2-20之间"
            )
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("邮箱格式不正确")
        return v


class UserCreate(UserBase):
    """用户创建模型"""

    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$", v):
            raise ValueError("密码必须包含至少一个字母和一个数字，长度至少为8位")
        return v


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


class UserUpdate(UserCreate):
    """用户信息更新模型"""

    notification_type: Optional[bool] = None
    frequency: Optional[str] = None


class DeleteUserRequest(BaseModel):
    """删除用户请求模型"""

    user_id: str

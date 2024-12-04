from pydantic import BaseModel, validator
from typing import Optional
import re

class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    phone: Optional[str] = None


    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('无效的手机号码格式')
        return v

class UserCreate(UserBase):
    """用户创建模型"""
    password: str

class User(UserBase):
    """用户信息模型"""
    id: int

    class Config:
        # 允许从ORM模型创建
        from_attributes = True

class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """令牌数据模型"""
    username: Optional[str] = None
  
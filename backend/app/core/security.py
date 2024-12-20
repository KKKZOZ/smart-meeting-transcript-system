from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 认证配置
# tokenUrl: 指定获取 token 的接口地址，这里对应 auth_router 中的 /login 接口
# 在 SwaggerUI 中：
# 1. 点击右上角的 "Authorize" 按钮
# 2. 在弹出的对话框中输入用户名和密码
# 3. 点击 "Authorize" 按钮完成认证
# 4. 之后的所有需要认证的接口都会自动带上 Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建JWT访问令牌
    :param data: 要编码的数据
    :param expires_delta: 过期时间增量
    :return: 编码后的JWT字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str):
    """
    验证密码
    :param plain_password: 明文密码
    :param hashed_password: 哈希后的密码
    :return: 验证结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """
    获取密码的哈希值
    :param password: 明文密码
    :return: 哈希后的密码
    """
    return pwd_context.hash(password)


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证信息",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证信息",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    user_id = decode_token(token)
    print(user_id)
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

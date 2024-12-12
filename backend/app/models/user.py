from app.db.base import Base
from sqlalchemy import Column, String


class User(Base):
    """
    用户数据模型
    定义用户在数据库中的表结构
    """

    __tablename__ = "users"

    # 用户ID，主键
    user_id = Column(String(50), primary_key=True, index=True)
    # 用户名，唯一索引
    username = Column(String(50), unique=True, index=True)
    # 密码哈希值
    hashed_password = Column(String(100))
    # 电话号码，唯一索引
    phone = Column(String(11), unique=True, index=True, nullable=True)

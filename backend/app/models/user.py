from app.db.base import Base
from sqlalchemy import Column, String, Boolean


class User(Base):
    """
    用户数据模型
    定义用户在数据库中的表结构
    """

    __tablename__ = "users"

    # 用户ID，主键
    user_id = Column(String(50), primary_key=True, index=True)
    # 用户名，唯一索引
    username = Column(String(100), unique=True, index=True, nullable=False)
    # 昵称，唯一索引
    nickname = Column(String(100), unique=True, index=True, nullable=False)
    # 密码哈希值
    hashed_password = Column(String(100))
    # email
    email = Column(String(255), unique=True, index=True, nullable=True)

    notification_type = Column(Boolean, default=True)

    frequency = Column(String(20))

    enabled = Column(Boolean, default=True)

    root = Column(Boolean, default=False)

    def __str__(self):
        return (
            f"User(user_id={self.user_id}, username={self.username}, "
            f"email={self.email}, notification_type={self.notification_type}, "
            f"frequency={self.frequency}, enabled={self.enabled})"
        )

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL)
# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    依赖函数，用于获取数据库会话
    使用yield可以确保会话被正确关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

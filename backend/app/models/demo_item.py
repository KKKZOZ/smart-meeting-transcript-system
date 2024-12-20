from sqlalchemy import Column, Integer, VARCHAR
from app.db.base import Base


class DemoItem(Base):
    """演示项数据模型"""

    __tablename__ = "demo_items"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(VARCHAR(255), nullable=True, default="")

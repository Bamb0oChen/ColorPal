"""收集记录 ORM 模型"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from app.database import Base


class UserCollection(Base):
    """用户颜色收集记录 - 存储已收集的颜色 ID"""
    __tablename__ = "user_collections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, default="default")

    # 已收集的颜色 ID 列表，用逗号分隔存储
    collected_ids = Column(Text, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

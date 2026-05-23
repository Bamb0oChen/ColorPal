"""照片记录 ORM 模型"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from app.database import Base


class PhotoRecord(Base):
    __tablename__ = "photo_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)

    # 分析结果
    image_base64 = Column(Text, nullable=True)
    dominant_color = Column(String, default="#CCCCCC")
    palette = Column(Text, default="[]")  # JSON 数组
    score = Column(Integer, default=0)
    comment = Column(String, default="")
    color_category = Column(String, default="neutral")
    saturation_level = Column(String, default="medium")
    brightness_level = Column(String, default="medium")

    # 地理位置
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    place_name = Column(String, nullable=True)

    # 关联任务
    task_id = Column(String, nullable=True)

    taken_at = Column(DateTime, default=datetime.utcnow)

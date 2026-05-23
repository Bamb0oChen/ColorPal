"""用户 ORM 模型"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nickname = Column(String, default="玩家")
    avatar_url = Column(String, default="")

    # 小人状态
    pet_name = Column(String, default="小彩")
    pet_stage = Column(Integer, default=0)
    pet_mood = Column(String, default="happy")
    pet_color = Column(String, default="#CCCCCC")

    # 能量
    energy_current = Column(Integer, default=50)
    energy_max = Column(Integer, default=300)
    energy_r = Column(Integer, default=20)
    energy_g = Column(Integer, default=15)
    energy_b = Column(Integer, default=15)

    # 统计
    total_photos = Column(Integer, default=0)
    highest_score = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_photo_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

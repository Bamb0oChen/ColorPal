from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    pet_stage = Column(Integer, default=1)
    pet_mood = Column(String, default="neutral")
    pet_color = Column(String, default="#CCCCCC")
    energy_current = Column(Integer, default=0)
    energy_max = Column(Integer, default=100)
    energy_r = Column(Integer, default=0)
    energy_g = Column(Integer, default=0)
    energy_b = Column(Integer, default=0)
    total_photos = Column(Integer, default=0)
    highest_score = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_photo_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

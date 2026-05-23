from sqlalchemy import Column, String, Integer, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class PhotoRecord(Base):
    __tablename__ = "photo_records"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    image_base64 = Column(Text, nullable=False)
    dominant_color = Column(String, nullable=False)
    palette = Column(JSON, nullable=False)
    score = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    color_category = Column(String, nullable=False)
    saturation_level = Column(String, nullable=False)
    brightness_level = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    place_name = Column(String, nullable=True)
    taken_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="photos")

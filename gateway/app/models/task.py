"""任务 ORM 模型"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)

    type = Column(String, default="color_collect")
    title = Column(String, default="")
    description = Column(String, default="")
    target_value = Column(String, default="")

    reward_energy = Column(Integer, default=50)
    status = Column(String, default="active")  # active / completed

    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

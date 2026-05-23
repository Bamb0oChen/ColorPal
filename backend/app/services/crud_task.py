"""任务 CRUD"""

import random
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task import Task

TASK_TEMPLATES = [
    {"type": "color_collect", "title": "我想看红色的东西", "description": "拍一张以红色为主色调的照片", "target": "#FF0000"},
    {"type": "color_collect", "title": "我想看蓝色的东西", "description": "拍一张以蓝色为主色调的照片", "target": "#0000FF"},
    {"type": "color_collect", "title": "我想看绿色的东西", "description": "拍一张以绿色为主色调的照片", "target": "#00FF00"},
    {"type": "warm", "title": "给我点温暖", "description": "拍一张暖色调的照片", "target": "warm"},
    {"type": "high_saturation", "title": "要鲜艳的！", "description": "拍一张高饱和度的照片", "target": "high"},
]


def get_current_task(db: Session, user_id: str) -> dict | None:
    """获取当前活跃任务"""
    task = (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.status == "active")
        .first()
    )
    if not task:
        return None
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "reward_energy": task.reward_energy,
        "status": task.status,
    }


def generate_task(db: Session, user_id: str) -> dict:
    """生成新任务"""
    # 先完成当前任务
    current = db.query(Task).filter(Task.user_id == user_id, Task.status == "active").all()
    for t in current:
        t.status = "expired"

    # 随机选一个模板
    template = random.choice(TASK_TEMPLATES)
    task = Task(
        user_id=user_id,
        type=template["type"],
        title=template["title"],
        description=template["description"],
        target_value=template["target"],
        reward_energy=50,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "reward_energy": task.reward_energy,
        "status": task.status,
    }

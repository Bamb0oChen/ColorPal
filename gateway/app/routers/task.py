"""任务路由"""

import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/task", tags=["task"])


@router.get("/current")
async def get_current_task():
    """获取当前任务"""
    return {
        "code": 0,
        "data": {
            "id": "task_001",
            "title": "我想看红色的东西",
            "description": "拍一张以红色为主色调的照片",
            "reward": {"energy_bonus": 50},
            "status": "active",
        },
        "message": "ok",
    }

"""用户路由"""

import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile")
async def get_profile():
    """获取用户信息和小人状态"""
    return {
        "code": 0,
        "data": {
            "nickname": "玩家",
            "avatar": "",
            "pet": {
                "name": "小彩",
                "stage": 0,
                "mood": "happy",
                "color": "#CCCCCC",
                "energy": {
                    "current": 50,
                    "max": 300,
                    "r": 20,
                    "g": 15,
                    "b": 15,
                },
            },
            "stats": {
                "total_photos": 0,
                "highest_score": 0,
                "streak_days": 0,
            },
        },
        "message": "ok",
    }

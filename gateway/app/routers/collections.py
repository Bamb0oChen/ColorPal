"""图鉴收集路由"""

from fastapi import APIRouter

router = APIRouter(prefix="/collections", tags=["collections"])

FAMILIES = [
    {"id": "red", "name": "红色系", "color": "#FF0000", "total": 6, "collected": 3},
    {"id": "orange", "name": "橙色系", "color": "#FFA500", "total": 4, "collected": 4},
    {"id": "yellow", "name": "黄色系", "color": "#FFD700", "total": 5, "collected": 2},
    {"id": "green", "name": "绿色系", "color": "#7CFC00", "total": 6, "collected": 1},
    {"id": "blue", "name": "蓝色系", "color": "#87CEEB", "total": 6, "collected": 5},
    {"id": "purple", "name": "紫色系", "color": "#8F00FF", "total": 5, "collected": 0},
    {"id": "gray", "name": "无彩色", "color": "#B2BEC3", "total": 4, "collected": 1},
]

TOTAL_COLORS = 36
TOTAL_COLLECTED = sum(family["collected"] for family in FAMILIES)


@router.get("/progress")
def collection_progress():
    """获取按色系汇总的图鉴进度"""
    return {
        "code": 0,
        "data": {
            "total_colors": TOTAL_COLORS,
            "total_collected": TOTAL_COLLECTED,
            "percent": round(TOTAL_COLLECTED / TOTAL_COLORS * 100, 1),
            "families": FAMILIES,
        },
        "message": "ok",
    }

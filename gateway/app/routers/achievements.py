"""成就路由"""

from fastapi import APIRouter

router = APIRouter(prefix="/achievements", tags=["achievements"])

# MVP 阶段先返回演示进度，后续由真实 collections 数据驱动。
ACHIEVEMENTS = [
    {
        "id": "red",
        "name": "红色狂热",
        "desc": "集齐全部6种红色系颜色",
        "icon": "red",
        "color": "#FF0000",
        "target": 6,
        "progress": 3,
        "unlocked": False,
    },
    {
        "id": "orange",
        "name": "橙色收集家",
        "desc": "集齐全部4种橙色系颜色",
        "icon": "orange",
        "color": "#FFA500",
        "target": 4,
        "progress": 4,
        "unlocked": True,
    },
    {
        "id": "yellow",
        "name": "黄色猎人",
        "desc": "集齐全部5种黄色系颜色",
        "icon": "yellow",
        "color": "#FFD700",
        "target": 5,
        "progress": 2,
        "unlocked": False,
    },
    {
        "id": "green",
        "name": "绿色守护者",
        "desc": "集齐全部6种绿色系颜色",
        "icon": "green",
        "color": "#7CFC00",
        "target": 6,
        "progress": 1,
        "unlocked": False,
    },
    {
        "id": "blue",
        "name": "蓝色梦想家",
        "desc": "集齐全部6种蓝色系颜色",
        "icon": "blue",
        "color": "#87CEEB",
        "target": 6,
        "progress": 5,
        "unlocked": False,
    },
    {
        "id": "purple",
        "name": "紫色神秘",
        "desc": "集齐全部5种紫色系颜色",
        "icon": "purple",
        "color": "#8F00FF",
        "target": 5,
        "progress": 0,
        "unlocked": False,
    },
    {
        "id": "gray",
        "name": "无彩大师",
        "desc": "集齐全部4种无彩色/金属色",
        "icon": "gray",
        "color": "#B2BEC3",
        "target": 4,
        "progress": 1,
        "unlocked": False,
    },
    {
        "id": "full",
        "name": "全色谱大师",
        "desc": "集齐全部36种颜色",
        "icon": "spectrum",
        "color": "#FFD700",
        "target": 36,
        "progress": 18,
        "unlocked": False,
    },
]


@router.get("")
def list_achievements():
    """获取成就列表和完成进度"""
    done = sum(1 for achievement in ACHIEVEMENTS if achievement["unlocked"])
    return {
        "code": 0,
        "data": {
            "total": len(ACHIEVEMENTS),
            "done": done,
            "list": ACHIEVEMENTS,
        },
        "message": "ok",
    }

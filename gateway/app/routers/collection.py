"""收集与成就路由"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.crud_collection import (
    get_collection_progress,
    get_user_collection,
    get_achievements,
    add_collected_color,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/collections", tags=["collection"])


@router.get("/progress")
def collection_progress(user_id: str = "default", db: Session = Depends(get_db)):
    """获取收集进度（按色系 + 总计）"""
    data = get_collection_progress(db, user_id)
    return {"code": 0, "data": data, "message": "ok"}


@router.get("/user")
def user_collection(user_id: str = "default", db: Session = Depends(get_db)):
    """获取用户已收集的颜色 ID 列表"""
    data = get_user_collection(db, user_id)
    return {"code": 0, "data": data, "message": "ok"}


@router.get("/achievements")
def achievements(user_id: str = "default", db: Session = Depends(get_db)):
    """获取成就列表 + 进度状态"""
    data = get_achievements(db, user_id)
    return {"code": 0, "data": data, "message": "ok"}

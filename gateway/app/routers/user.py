"""用户路由"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.crud_user import get_profile

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile")
def profile(user_id: str = "default", db: Session = Depends(get_db)):
    """获取用户信息和小人状态"""
    data = get_profile(db, user_id)
    return {"code": 0, "data": data, "message": "ok"}

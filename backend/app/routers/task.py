"""任务路由。"""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.crud_task import get_current_task, generate_task

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/task', tags=['task'])


@router.get('/current')
def current_task(user_id: str = 'default', db: Session = Depends(get_db)):
    """获取当前活跃任务。"""
    task = get_current_task(db, user_id)
    return {
        'code': 0,
        'data': task,
        'message': 'ok',
    }


@router.post('/generate')
def new_task(user_id: str = 'default', db: Session = Depends(get_db)):
    """生成新任务。"""
    task = generate_task(db, user_id)
    return {
        'code': 0,
        'data': task,
        'message': 'ok',
    }

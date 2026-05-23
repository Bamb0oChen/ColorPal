"""用户路由。"""

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.crud_user import get_profile

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/user', tags=['user'])


class EnergyUpdate(BaseModel):
    r: int = 0
    g: int = 0
    b: int = 0
    total: int = 0


@router.get('/profile')
def profile(user_id: str = 'default', db: Session = Depends(get_db)):
    """获取用户信息和小人状态。"""
    data = get_profile(db, user_id)
    return {'code': 0, 'data': data, 'message': 'ok'}


@router.post('/energy')
def update_energy(body: EnergyUpdate, user_id: str = 'default', db: Session = Depends(get_db)):
    """更新用户能量和累计经验值。"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    user.energy_r += body.r
    user.energy_g += body.g
    user.energy_b += body.b
    user.energy_current += body.total
    user.total_energy += body.total
    db.commit()
    db.refresh(user)

    return {
        'code': 0,
        'data': {
            'energy': {
                'current': user.energy_current,
                'max': user.energy_max,
                'r': user.energy_r,
                'g': user.energy_g,
                'b': user.energy_b,
            },
            'totalEnergy': user.total_energy,
        },
        'message': 'ok',
    }

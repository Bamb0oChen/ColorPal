"""用户 CRUD"""

from sqlalchemy.orm import Session
from app.models.user import User


def get_or_create_user(db: Session, user_id: str = "default") -> User:
    """获取或创建用户（MVP 阶段单用户模式）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_profile(db: Session, user_id: str = "default") -> dict:
    """组装用户主页信息"""
    user = get_or_create_user(db, user_id)
    return {
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "pet": {
            "name": user.pet_name,
            "stage": user.pet_stage,
            "mood": user.pet_mood,
            "color": user.pet_color,
            "energy": {
                "current": user.energy_current,
                "max": user.energy_max,
                "r": user.energy_r,
                "g": user.energy_g,
                "b": user.energy_b,
            },
        },
        "stats": {
            "total_photos": user.total_photos,
            "highest_score": user.highest_score,
            "streak_days": user.streak_days,
        },
    }

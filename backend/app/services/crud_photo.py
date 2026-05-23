"""照片 CRUD。"""

import json

from sqlalchemy.orm import Session

from app.models.photo import PhotoRecord
from app.models.user import User


def save_photo(
    db: Session,
    user_id: str,
    analysis: dict,
    image_base64: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    place_name: str | None = None,
    task_id: str | None = None,
) -> dict:
    """保存照片分析结果，更新用户能量。"""
    photo = PhotoRecord(
        user_id=user_id,
        image_base64=image_base64,
        dominant_color=analysis.get('dominant_color', '#CCCCCC'),
        palette=json.dumps(analysis.get('palette', [])),
        score=analysis.get('score', 0),
        comment=analysis.get('comment', ''),
        color_category=analysis.get('color_category', 'neutral'),
        saturation_level=analysis.get('saturation_level', 'medium'),
        brightness_level=analysis.get('brightness_level', 'medium'),
        latitude=latitude,
        longitude=longitude,
        place_name=place_name,
        task_id=task_id,
    )
    db.add(photo)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        db.add(user)
        db.flush()

    hex_color = analysis.get('dominant_color', '#CCCCCC')
    value = int(hex_color.lstrip('#'), 16)
    r_inc = ((value >> 16) & 255) // 10
    g_inc = ((value >> 8) & 255) // 10
    b_inc = (value & 255) // 10

    user.energy_r += r_inc
    user.energy_g += g_inc
    user.energy_b += b_inc
    user.energy_current = user.energy_r + user.energy_g + user.energy_b
    user.pet_color = hex_color
    user.total_photos += 1
    user.last_photo_at = photo.taken_at

    score = analysis.get('score', 0)
    if score > user.highest_score:
        user.highest_score = score

    # 心情由最近 5 张照片决定，避免单张低分让小人状态剧烈跳变。
    recent = (
        db.query(PhotoRecord.score)
        .filter(PhotoRecord.user_id == user_id)
        .order_by(PhotoRecord.taken_at.desc())
        .limit(5)
        .all()
    )
    avg_score = sum(s for (s,) in recent) / max(len(recent), 1)
    user.pet_mood = 'happy' if avg_score >= 70 else 'neutral' if avg_score >= 40 else 'sad'

    db.commit()
    db.refresh(photo)

    return {
        'id': photo.id,
        'energy_change': {
            'r': r_inc,
            'g': g_inc,
            'b': b_inc,
            'total': r_inc + g_inc + b_inc,
        },
    }


def get_photo_list(db: Session, user_id: str, page: int = 1, limit: int = 20) -> dict:
    """获取照片列表。"""
    query = (
        db.query(PhotoRecord)
        .filter(PhotoRecord.user_id == user_id)
        .order_by(PhotoRecord.taken_at.desc())
    )
    total = query.count()
    photos = query.offset((page - 1) * limit).limit(limit).all()

    return {
        'photos': [
            {
                'id': p.id,
                'dominant_color': p.dominant_color,
                'score': p.score,
                'comment': p.comment,
                'taken_at': p.taken_at.isoformat() if p.taken_at else '',
            }
            for p in photos
        ],
        'total': total,
        'page': page,
    }


def get_map_points(db: Session, user_id: str) -> list:
    """获取有地理位置的照片（地图标记点）。"""
    photos = (
        db.query(PhotoRecord)
        .filter(
            PhotoRecord.user_id == user_id,
            PhotoRecord.latitude.isnot(None),
            PhotoRecord.longitude.isnot(None),
        )
        .all()
    )
    return [
        {
            'photo_id': p.id,
            'lat': p.latitude,
            'lng': p.longitude,
            'color': p.dominant_color,
            'score': p.score,
        }
        for p in photos
    ]

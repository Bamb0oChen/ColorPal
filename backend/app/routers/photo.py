"""照片分析路由。"""

import logging

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.ai_analyzer import analyze_image
from app.services.crud_photo import save_photo, get_photo_list, get_map_points

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/photo', tags=['photo'])

ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/webp'}


@router.post("/analyze")
async def analyze_photo(
    image: UploadFile = File(...),
    lat: float | None = Form(None),
    lng: float | None = Form(None),
    place_name: str | None = Form(None),
    user_id: str = Form('default'),
    db: Session = Depends(get_db),
):
    """上传照片 -> AI 分析 -> 存储 -> 返回评分 + 能量变化。"""
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail='仅支持 JPEG/PNG/WebP')

    try:
        image_bytes = await image.read()

        analysis = await analyze_image(image_bytes)
        saved = save_photo(
            db=db,
            user_id=user_id,
            analysis=analysis,
            image_base64=None,  # MVP 阶段不存原图
            latitude=lat,
            longitude=lng,
            place_name=place_name,
        )

        return {
            'code': 0,
            'data': {
                'photo_id': saved['id'],
                'analysis': analysis,
                'energy_change': saved['energy_change'],
                'task_completed': None,
            },
            'message': 'ok',
        }

    except Exception as err:
        logger.exception('照片分析失败')
        raise HTTPException(status_code=500, detail=f'分析失败: {str(err)}') from err


@router.get('/list')
def list_photos(
    page: int = 1,
    limit: int = 20,
    user_id: str = 'default',
    db: Session = Depends(get_db),
):
    """获取用户照片列表。"""
    return {'code': 0, 'data': get_photo_list(db, user_id, page, limit), 'message': 'ok'}


@router.get('/map-points')
def map_points(user_id: str = 'default', db: Session = Depends(get_db)):
    """获取有位置信息的照片（地图标记点）。"""
    return {'code': 0, 'data': get_map_points(db, user_id), 'message': 'ok'}

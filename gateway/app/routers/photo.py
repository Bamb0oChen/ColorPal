"""照片分析路由"""

import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/photo", tags=["photo"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/analyze")
async def analyze_photo(
    image: UploadFile = File(...),
    lat: float = Form(None),
    lng: float = Form(None),
):
    """上传照片并分析颜色"""
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="不支持的图片格式，仅支持 JPEG/PNG/WebP")

    try:
        image_bytes = await image.read()

        # TODO: 调用 AI 分析 (B 负责对接)
        # TODO: 转发结果到 C# 后端 (C 负责对接)

        return {
            "code": 0,
            "data": {
                "photo_id": "temp_id",
                "analysis": {
                    "dominant_color": "#4ECDC4",
                    "palette": ["#4ECDC4", "#FF6B6B", "#FFE66D"],
                    "score": 75,
                    "comment": "待接入 AI 分析",
                    "color_category": "cool",
                    "saturation_level": "medium",
                    "brightness_level": "high",
                },
                "energy_change": {"r": 15, "g": 25, "b": 20, "total": 60},
                "task_completed": None,
            },
            "message": "ok",
        }

    except Exception as err:
        logger.exception("照片分析失败")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(err)}")

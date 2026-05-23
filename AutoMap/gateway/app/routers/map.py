from fastapi import APIRouter, HTTPException
from app.models.map import RecommendRequest, RecommendResponse, LocationResponse
from app.services.recommender import get_recommendations
from app.services.backend_client import get_location_from_backend
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/map", tags=["map"])


@router.post("/recommend", response_model=RecommendResponse)
async def recommend_places(request: RecommendRequest):
    try:
        result = await get_recommendations(request.query, request.location)
        return result
    except Exception as e:
        logger.error(f"推荐失败: {e}")
        raise HTTPException(status_code=500, detail="推荐服务暂时不可用")


@router.get("/location", response_model=LocationResponse)
async def get_current_location():
    try:
        return LocationResponse(
            lat=31.2304,
            lng=121.4737,
            address="上海市黄浦区"
        )
    except Exception as e:
        logger.error(f"获取位置失败: {e}")
        raise HTTPException(status_code=500, detail="位置服务暂时不可用")

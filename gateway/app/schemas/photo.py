"""照片相关 Pydantic schema"""

from pydantic import BaseModel, Field
from typing import Optional


class AnalysisResult(BaseModel):
    dominant_color: str = Field(default="#CCCCCC", pattern=r"^#[0-9a-fA-F]{6}$")
    palette: list[str] = []
    score: int = Field(default=50, ge=0, le=100)
    comment: str = ""
    color_category: str = "neutral"
    saturation_level: str = "medium"
    brightness_level: str = "medium"


class PhotoAnalyzeResponse(BaseModel):
    photo_id: str
    analysis: AnalysisResult
    energy_change: dict
    task_completed: Optional[str] = None


class MapPoint(BaseModel):
    photo_id: str
    lat: float
    lng: float
    color: str
    score: int


class PhotoListItem(BaseModel):
    id: str
    dominant_color: str
    score: int
    comment: str
    taken_at: str

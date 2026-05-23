from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class AnalysisResult(BaseModel):
    dominantColor: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$")
    palette: List[str]
    score: int = Field(..., ge=0, le=100)
    comment: str
    colorCategory: Literal["warm", "cool", "neutral"]
    saturationLevel: Literal["high", "medium", "low"]
    brightnessLevel: Literal["high", "medium", "low"]


class PhotoRecord(BaseModel):
    id: str
    userId: str
    dominantColor: str
    palette: List[str]
    score: int
    comment: Optional[str]
    colorCategory: str
    saturationLevel: str
    brightnessLevel: str
    latitude: Optional[float]
    longitude: Optional[float]
    placeName: Optional[str]
    takenAt: datetime

    class Config:
        from_attributes = True

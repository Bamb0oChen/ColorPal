from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: str
    nickname: str
    avatar: Optional[str]
    petStage: int
    petMood: str
    petColor: str
    energyCurrent: int
    energyMax: int
    energyR: int
    energyG: int
    energyB: int
    totalPhotos: int
    highestScore: int
    streakDays: int
    lastPhotoAt: Optional[datetime]
    createdAt: datetime

    class Config:
        from_attributes = True

"""用户相关 Pydantic schema"""

from pydantic import BaseModel


class PetInfo(BaseModel):
    name: str = "小彩"
    stage: int = 0
    mood: str = "happy"
    color: str = "#CCCCCC"
    energy: dict = {"current": 50, "max": 300, "r": 20, "g": 15, "b": 15}


class UserProfile(BaseModel):
    nickname: str
    avatar_url: str
    pet: PetInfo
    stats: dict

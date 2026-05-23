"""社区 Pydantic schema"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CommunityUser(BaseModel):
    id: str
    nickname: str
    avatar: str = ""

    class Config:
        from_attributes = True


class CommunityPost(BaseModel):
    id: str
    user: CommunityUser
    content: Optional[str] = None
    images: Optional[list[str]] = None
    likeCount: int = 0
    commentCount: int = 0
    liked: bool = False
    createdAt: datetime

    class Config:
        from_attributes = True


class CommunityComment(BaseModel):
    id: str
    user: CommunityUser
    content: str
    createdAt: datetime

    class Config:
        from_attributes = True


class CreateCommentRequest(BaseModel):
    content: str


class LikeResponse(BaseModel):
    liked: bool
    likeCount: int


class ApiResponse(BaseModel):
    code: int = 0
    data: Optional[list | dict] = None
    message: str = "ok"

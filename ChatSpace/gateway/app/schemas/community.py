from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CommunityUser(BaseModel):
    id: str
    nickname: str
    avatar: str

    class Config:
        from_attributes = True


class PhotoRecordSummary(BaseModel):
    dominantColor: str
    palette: List[str]
    score: int

    class Config:
        from_attributes = True


class CommunityPost(BaseModel):
    id: str
    user: CommunityUser
    content: Optional[str]
    images: Optional[List[str]]
    photoRecord: Optional[PhotoRecordSummary]
    likeCount: int
    commentCount: int
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


class CreatePostRequest(BaseModel):
    content: Optional[str] = None


class CreateCommentRequest(BaseModel):
    content: str


class LikeResponse(BaseModel):
    liked: bool
    likeCount: int


class ApiResponse(BaseModel):
    code: int = 0
    data: Optional[dict] = None
    message: str = "ok"

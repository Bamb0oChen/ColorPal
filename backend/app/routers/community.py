"""社区帖子/评论/点赞 API"""

import uuid
import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import User
from app.models.community import CommunityPost, CommunityComment, CommunityLike

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
STATIC_URL = "/uploads"
from app.schemas.community import (
    CommunityPost as CommunityPostSchema,
    CommunityComment as CommunityCommentSchema,
    CommunityUser as CommunityUserSchema,
    CreateCommentRequest,
    LikeResponse,
    ApiResponse,
)

router = APIRouter(prefix="/community", tags=["community"])


def get_or_create_user(db: Session, user_id: str, nickname: str = "玩家") -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(
            id=user_id,
            nickname=nickname,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.nickname != nickname:
        user.nickname = nickname
        db.commit()
        db.refresh(user)
    return user


def user_to_schema(user: User) -> CommunityUserSchema:
    return CommunityUserSchema(
        id=user.id,
        nickname=user.nickname or "玩家",
        avatar=user.avatar_url or "",
    )


def post_to_schema(post: CommunityPost, liked: bool = False) -> CommunityPostSchema:
    return CommunityPostSchema(
        id=post.id,
        user=user_to_schema(post.user),
        content=post.content,
        images=post.images or [],
        likeCount=post.like_count or 0,
        commentCount=post.comment_count or 0,
        liked=liked,
        createdAt=post.created_at,
    )


@router.get("/posts/mine")
async def list_my_posts(
    x_user_id: str = Header(default="user_001"),
    x_user_name: str = Header(default="玩家"),
    db: Session = Depends(get_db),
):
    """获取当前用户的帖子。"""
    user = get_or_create_user(db, x_user_id, x_user_name)
    posts = (
        db.query(CommunityPost)
        .filter(CommunityPost.user_id == user.id)
        .order_by(desc(CommunityPost.created_at))
        .limit(50)
        .all()
    )
    return ApiResponse(
        data=[post_to_schema(p).model_dump(mode="json") for p in posts],
    ).model_dump()


@router.get("/posts")
async def list_posts(db: Session = Depends(get_db)):
    posts = db.query(CommunityPost).order_by(desc(CommunityPost.created_at)).limit(50).all()
    return ApiResponse(
        data=[post_to_schema(p).model_dump(mode="json") for p in posts],
    ).model_dump()


@router.get("/posts/{post_id}")
async def get_post(post_id: str, db: Session = Depends(get_db)):
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    return ApiResponse(
        data=post_to_schema(post).model_dump(mode="json"),
    ).model_dump()


@router.post("/posts")
async def create_post(
    x_user_id: str = Header(default="user_001"),
    x_user_name: str = Header(default="玩家"),
    content: str = Form(default=""),
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    user = get_or_create_user(db, x_user_id, x_user_name)

    image_urls: list[str] = []
    for img in images:
        ext = os.path.splitext(img.filename or ".jpg")[1] or ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = UPLOAD_DIR / filename
        content_bytes = await img.read()
        filepath.write_bytes(content_bytes)
        image_urls.append(f"http://127.0.0.1:8000{STATIC_URL}/{filename}")

    post = CommunityPost(
        id=str(uuid.uuid4()),
        user_id=user.id,
        content=content or None,
        images=image_urls or None,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return ApiResponse(
        data=post_to_schema(post).model_dump(mode="json"),
    ).model_dump()


@router.post("/posts/{post_id}/like")
async def toggle_like(
    post_id: str,
    x_user_id: str = Header(default="user_001"),
    x_user_name: str = Header(default="玩家"),
    db: Session = Depends(get_db),
):
    user = get_or_create_user(db, x_user_id, x_user_name)
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    existing = (
        db.query(CommunityLike)
        .filter(CommunityLike.post_id == post_id, CommunityLike.user_id == user.id)
        .first()
    )

    if existing:
        db.delete(existing)
        post.like_count = max(0, (post.like_count or 0) - 1)
        liked = False
    else:
        like = CommunityLike(id=str(uuid.uuid4()), post_id=post_id, user_id=user.id)
        db.add(like)
        post.like_count = (post.like_count or 0) + 1
        liked = True

    db.commit()
    db.refresh(post)
    return ApiResponse(
        data=LikeResponse(liked=liked, likeCount=post.like_count or 0).model_dump(),
    ).model_dump()


@router.get("/posts/{post_id}/comments")
async def list_comments(post_id: str, db: Session = Depends(get_db)):
    comments = (
        db.query(CommunityComment)
        .filter(CommunityComment.post_id == post_id)
        .order_by(CommunityComment.created_at)
        .all()
    )
    result = []
    for c in comments:
        result.append(
            CommunityCommentSchema(
                id=c.id,
                user=user_to_schema(c.user),
                content=c.content,
                createdAt=c.created_at,
            ).model_dump(mode="json")
        )
    return ApiResponse(data=result).model_dump()


@router.post("/posts/{post_id}/comments")
async def create_comment(
    post_id: str,
    body: CreateCommentRequest,
    x_user_id: str = Header(default="user_001"),
    x_user_name: str = Header(default="玩家"),
    db: Session = Depends(get_db),
):
    user = get_or_create_user(db, x_user_id, x_user_name)
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    comment = CommunityComment(
        id=str(uuid.uuid4()),
        post_id=post_id,
        user_id=user.id,
        content=body.content,
    )
    db.add(comment)
    post.comment_count = (post.comment_count or 0) + 1
    db.commit()
    db.refresh(comment)

    return ApiResponse(
        data=CommunityCommentSchema(
            id=comment.id,
            user=user_to_schema(comment.user),
            content=comment.content,
            createdAt=comment.created_at,
        ).model_dump(mode="json"),
    ).model_dump()


# ---- 开发者注入接口 ----

@router.post("/dev/inject")
async def inject_posts(
    x_user_id: str = Header(default="dev_inject"),
    db: Session = Depends(get_db),
):
    """为开发者批量注入示例帖子，方便前端调试。"""
    user = get_or_create_user(db, x_user_id, "开发者")
    posts_data = [
        "今天的日落太美了，天边从橙色渐变到紫色，像一块打翻的调色板",
        "路边的涂鸦墙，蓝色和粉色的碰撞意外地和谐，果断拍照记录！",
        "新买的多肉植物，叶尖带着淡淡的粉红色，自然的配色永远是最舒服的。",
        "下雨天，窗外的世界褪成了灰色调，安静又治愈。",
        "街角的咖啡店，暖黄色的灯光透过玻璃窗洒在人行道上，温暖了整个夜晚。",
        "秋天的银杏叶铺满地面，金黄一片，踩上去沙沙作响。",
    ]

    created = []
    for text in posts_data:
        post = CommunityPost(
            id=str(uuid.uuid4()),
            user_id=user.id,
            content=text,
        )
        db.add(post)
        db.flush()
        db.refresh(post)
        created.append(post_to_schema(post).model_dump(mode="json"))

    db.commit()
    return ApiResponse(data=created).model_dump()

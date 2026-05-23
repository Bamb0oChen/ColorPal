import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import CommunityPost, CommunityComment, CommunityLike, User, PhotoRecord
from app.schemas.community import (
    CommunityPost as CommunityPostSchema,
    CommunityComment as CommunityCommentSchema,
    CommunityUser as CommunityUserSchema,
    PhotoRecordSummary,
    CreateCommentRequest,
    LikeResponse
)

router = APIRouter()

MOCK_USER_ID = "user_001"


def get_or_create_mock_user(db: Session) -> User:
    user = db.query(User).filter(User.id == MOCK_USER_ID).first()
    if not user:
        user = User(
            id=MOCK_USER_ID,
            nickname="色彩探险家",
            avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=colorpal"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def user_to_schema(user: User) -> CommunityUserSchema:
    return CommunityUserSchema(
        id=user.id,
        nickname=user.nickname,
        avatar=user.avatar or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
    )


def post_to_schema(post: CommunityPost, current_user_id: str, db: Session) -> CommunityPostSchema:
    liked = db.query(CommunityLike).filter(
        CommunityLike.post_id == post.id,
        CommunityLike.user_id == current_user_id
    ).first() is not None

    photo_summary = None
    if post.photo_record:
        photo_summary = PhotoRecordSummary(
            dominantColor=post.photo_record.dominant_color,
            palette=post.photo_record.palette,
            score=post.photo_record.score
        )

    return CommunityPostSchema(
        id=post.id,
        user=user_to_schema(post.user),
        content=post.content,
        images=post.images,
        photoRecord=photo_summary,
        likeCount=post.like_count,
        commentCount=post.comment_count,
        liked=liked,
        createdAt=post.created_at
    )


@router.get("/community/posts", response_model=dict)
def get_posts(db: Session = Depends(get_db)):
    user = get_or_create_mock_user(db)
    posts = db.query(CommunityPost).order_by(desc(CommunityPost.created_at)).all()
    post_schemas = [post_to_schema(p, user.id, db) for p in posts]
    return {"code": 0, "data": post_schemas, "message": "ok"}


@router.get("/community/posts/{post_id}", response_model=dict)
def get_post(post_id: str, db: Session = Depends(get_db)):
    user = get_or_create_mock_user(db)
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"code": 0, "data": post_to_schema(post, user.id, db), "message": "ok"}


@router.post("/community/posts", response_model=dict)
def create_post(
    content: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    photoRecordId: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    user = get_or_create_mock_user(db)

    image_urls = []
    if images:
        for img in images:
            image_urls.append(f"https://picsum.photos/seed/{uuid.uuid4()}/400/300")

    photo_record = None
    if photoRecordId:
        photo_record = db.query(PhotoRecord).filter(PhotoRecord.id == photoRecordId).first()

    post = CommunityPost(
        id=str(uuid.uuid4()),
        user_id=user.id,
        content=content,
        images=image_urls if image_urls else None,
        photo_record_id=photoRecordId if photo_record else None
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {"code": 0, "data": post_to_schema(post, user.id, db), "message": "ok"}


@router.post("/community/posts/{post_id}/like", response_model=dict)
def toggle_like(post_id: str, db: Session = Depends(get_db)):
    user = get_or_create_mock_user(db)
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = db.query(CommunityLike).filter(
        CommunityLike.post_id == post_id,
        CommunityLike.user_id == user.id
    ).first()

    if existing_like:
        db.delete(existing_like)
        post.like_count = max(0, post.like_count - 1)
        liked = False
    else:
        like = CommunityLike(id=str(uuid.uuid4()), post_id=post_id, user_id=user.id)
        db.add(like)
        post.like_count += 1
        liked = True

    db.commit()
    return {"code": 0, "data": {"liked": liked, "likeCount": post.like_count}, "message": "ok"}


@router.get("/community/posts/{post_id}/comments", response_model=dict)
def get_comments(post_id: str, db: Session = Depends(get_db)):
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = db.query(CommunityComment).filter(
        CommunityComment.post_id == post_id
    ).order_by(CommunityComment.created_at).all()

    comment_schemas = [
        CommunityCommentSchema(
            id=c.id,
            user=user_to_schema(c.user),
            content=c.content,
            createdAt=c.created_at
        )
        for c in comments
    ]

    return {"code": 0, "data": comment_schemas, "message": "ok"}


@router.post("/community/posts/{post_id}/comments", response_model=dict)
def create_comment(
    post_id: str,
    request: CreateCommentRequest,
    db: Session = Depends(get_db)
):
    user = get_or_create_mock_user(db)
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = CommunityComment(
        id=str(uuid.uuid4()),
        post_id=post_id,
        user_id=user.id,
        content=request.content
    )

    db.add(comment)
    post.comment_count += 1
    db.commit()
    db.refresh(comment)

    return {
        "code": 0,
        "data": CommunityCommentSchema(
            id=comment.id,
            user=user_to_schema(comment.user),
            content=comment.content,
            createdAt=comment.created_at
        ),
        "message": "ok"
    }

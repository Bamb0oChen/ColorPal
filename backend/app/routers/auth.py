"""GitHub Discussions based lightweight login endpoints."""

from datetime import UTC, datetime
from uuid import uuid4

import httpx
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.config import settings

router = APIRouter(prefix='/auth', tags=['auth'])


class DiscussionLoginStart(BaseModel):
    provider: str = 'github_discussions'
    discussion_url: str
    is_reachable: bool


class DiscussionLoginRequest(BaseModel):
    display_name: str = Field(default='Color walker', max_length=40)
    discussion_url: str | None = None


class UserSession(BaseModel):
    user_id: str
    display_name: str
    provider: str
    discussion_url: str
    created_at: str


@router.get('/github-discussion/start', response_model=DiscussionLoginStart)
async def start_github_discussion_login() -> DiscussionLoginStart:
    """Return the configured discussion URL and verify that GitHub is reachable when possible."""
    is_reachable = False
    try:
        async with httpx.AsyncClient(timeout=3, follow_redirects=True) as client:
            response = await client.get(settings.github_discussion_url)
            is_reachable = response.status_code < 500
    except httpx.HTTPError:
        # The login surface should remain usable during local demos without network access.
        is_reachable = False

    return DiscussionLoginStart(
        discussion_url=settings.github_discussion_url,
        is_reachable=is_reachable,
    )


@router.post('/github-discussion/login', response_model=UserSession)
async def complete_github_discussion_login(payload: DiscussionLoginRequest) -> UserSession:
    """Create a local session after the user enters from the GitHub Discussions login path."""
    display_name = payload.display_name.strip() or 'Color walker'
    return UserSession(
        user_id=f'gh-discussion-{uuid4().hex[:12]}',
        display_name=display_name,
        provider='github_discussions',
        discussion_url=payload.discussion_url or settings.github_discussion_url,
        created_at=datetime.now(UTC).isoformat(),
    )

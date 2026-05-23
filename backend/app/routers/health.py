"""Health check endpoint shared by local dev and containers."""

from fastapi import APIRouter

router = APIRouter(tags=['health'])


@router.get('/health')
async def health_check() -> dict[str, str]:
    return {'status': 'ok', 'service': 'colorpal-backend'}

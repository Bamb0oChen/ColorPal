"""健康检查端点；前后端联调与容器探活共用。"""

from fastapi import APIRouter

router = APIRouter(tags=['health'])


@router.get('/health')
async def health_check() -> dict[str, str]:
    return {'status': 'ok', 'service': 'colorpal-backend'}

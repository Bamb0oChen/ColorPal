"""ColorPal FastAPI 入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health

app = FastAPI(
    title='ColorPal API',
    version='0.1.0',
    description='ColorPal 后端：AI 颜色分析 + 持久化',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router, prefix='/api/v1')


@app.get('/')
async def root() -> dict[str, str]:
    return {'service': 'colorpal-backend', 'docs': '/docs'}

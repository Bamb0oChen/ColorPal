"""ColorPal FastAPI 入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import agent, health, photo, task, user

app = FastAPI(
    title='ColorPal API',
    version='0.2.0',
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
app.include_router(photo.router, prefix='/api/v1')
app.include_router(user.router, prefix='/api/v1')
app.include_router(task.router, prefix='/api/v1')
app.include_router(agent.router, prefix='/api/v1')


@app.on_event('startup')
async def startup() -> None:
    """MVP 阶段用自动建表降低演示环境启动成本。"""
    init_db()


@app.get('/')
async def root() -> dict[str, str]:
    return {'service': 'colorpal-backend', 'docs': '/docs'}

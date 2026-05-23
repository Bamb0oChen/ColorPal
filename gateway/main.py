"""ColorPal FastAPI 入口"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import photo, user, task

app = FastAPI(title="ColorPal API", description="你的色彩伙伴", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(photo.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(task.router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    """应用启动时初始化数据库"""
    init_db()


@app.get("/health")
def health():
    return {"status": "ok", "service": "colopal-gateway"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

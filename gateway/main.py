"""ColorPal FastAPI 网关入口"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import photo, user, task
from app.core.config import settings

app = FastAPI(
    title="ColorPal API",
    description="ColorPal 中间层网关 — 前端入口",
    version="1.0.0",
)

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


@app.get("/health")
async def health():
    return {"status": "ok", "service": "colopal-gateway"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

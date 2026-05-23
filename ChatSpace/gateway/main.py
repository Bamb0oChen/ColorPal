from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import community, photo, user, task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ColorPal API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(community.router, prefix="/api/v1", tags=["community"])
app.include_router(photo.router, prefix="/api/v1", tags=["photo"])
app.include_router(user.router, prefix="/api/v1", tags=["user"])
app.include_router(task.router, prefix="/api/v1", tags=["task"])


@app.get("/")
def root():
    return {"message": "ColorPal API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import APIRouter

router = APIRouter()


@router.get("/task/current")
def get_current_task():
    return {"code": 0, "data": [], "message": "ok"}

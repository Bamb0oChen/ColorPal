from fastapi import APIRouter

router = APIRouter()


@router.get("/user/profile")
def get_profile():
    return {"code": 0, "data": {}, "message": "ok"}

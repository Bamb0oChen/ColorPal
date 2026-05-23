from fastapi import APIRouter

router = APIRouter()


@router.get("/photo/map-points")
def get_map_points():
    return {"code": 0, "data": [], "message": "ok"}


@router.get("/photo/list")
def get_photo_list():
    return {"code": 0, "data": [], "message": "ok"}

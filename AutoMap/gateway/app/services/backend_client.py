import httpx
from app.config import settings


async def get_location_from_backend():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{settings.backend_base_url}/api/location",
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise Exception(f"无法连接后端: {e}")


async def save_place_to_backend(place_data: dict):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{settings.backend_base_url}/api/places",
                json=place_data,
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise Exception(f"无法连接后端: {e}")

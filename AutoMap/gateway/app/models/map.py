from pydantic import BaseModel
from typing import Optional, List


class Location(BaseModel):
    lat: float
    lng: float


class Place(BaseModel):
    id: str
    name: str
    address: str
    location: Location
    category: str
    rating: float
    description: str
    image: str
    distance: float
    duration: Optional[str] = None


class RecommendRequest(BaseModel):
    query: str
    location: Optional[Location] = None


class RecommendResponse(BaseModel):
    places: List[Place]
    centerLocation: Location


class LocationResponse(BaseModel):
    lat: float
    lng: float
    address: str

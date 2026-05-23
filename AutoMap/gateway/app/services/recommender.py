import random
from typing import Optional
from app.models.map import RecommendResponse, Location, Place


sample_places = [
    {
        "id": "1",
        "name": "外滩",
        "address": "上海市黄浦区中山东一路",
        "location": {"lat": 31.2397, "lng": 121.4998},
        "category": "scenic",
        "rating": 4.8,
        "description": "百年历史万国建筑博览群，夜景超美，魔都地标必打卡",
        "image": "https://images.unsplash.com/photo-1474181487882-5abf3f0ba6a2?w=400",
        "distance": 1200,
        "duration": "20分钟",
    },
    {
        "id": "2",
        "name": "南京路步行街",
        "address": "上海市黄浦区南京东路",
        "location": {"lat": 31.2354, "lng": 121.4739},
        "category": "shopping",
        "rating": 4.5,
        "description": "中华商业第一街，老式铛铛车穿梭，购物美食一站式",
        "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
        "distance": 800,
        "duration": "12分钟",
    },
    {
        "id": "3",
        "name": "豫园",
        "address": "上海市黄浦区福佑路168号",
        "location": {"lat": 31.2220, "lng": 121.4880},
        "category": "scenic",
        "rating": 4.6,
        "description": "明代古典园林，九曲桥、小笼包，老上海味道",
        "image": "https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=400",
        "distance": 2100,
        "duration": "35分钟",
    },
    {
        "id": "4",
        "name": "东方明珠",
        "address": "上海市浦东新区世纪大道1号",
        "location": {"lat": 31.2397, "lng": 121.4998},
        "category": "scenic",
        "rating": 4.7,
        "description": "上海地标塔，360度俯瞰浦江两岸，悬空走廊超刺激",
        "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400",
        "distance": 1800,
        "duration": "25分钟",
    },
    {
        "id": "5",
        "name": "老城隍庙小吃广场",
        "address": "上海市黄浦区旧校场路99号",
        "location": {"lat": 31.2240, "lng": 121.4860},
        "category": "food",
        "rating": 4.4,
        "description": "南翔小笼、生煎包、蟹粉豆腐，上海小吃一网打尽",
        "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
        "distance": 1900,
        "duration": "30分钟",
    },
]


async def get_recommendations(query: str, location: Optional[Location] = None) -> RecommendResponse:
    center = location or Location(lat=31.2304, lng=121.4737)

    selected_places = []
    for i, place in enumerate(sample_places):
        place_copy = place.copy()
        variation = random.uniform(-0.01, 0.01)
        place_copy["location"] = {
            "lat": center.lat + variation * (i + 1),
            "lng": center.lng + variation * (i + 1)
        }
        place_copy["distance"] = random.randint(500, 3000)
        selected_places.append(Place(**place_copy))

    return RecommendResponse(
        places=selected_places,
        centerLocation=center
    )

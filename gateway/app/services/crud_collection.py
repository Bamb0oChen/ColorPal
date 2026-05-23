"""
收集与成就 CRUD
36 色数据、用户收集状态、成就判定
"""

from sqlalchemy.orm import Session
from app.models.collection import UserCollection

# ============================================================
# 36 色静态数据（与前端 constants.ts 对齐）
# ============================================================

COLOR_FAMILIES = [
    {"id": "red",    "name": "红色系", "color": "#FF0000", "total": 6},
    {"id": "orange", "name": "橙色系", "color": "#FFA500", "total": 4},
    {"id": "yellow", "name": "黄色系", "color": "#FFD700", "total": 5},
    {"id": "green",  "name": "绿色系", "color": "#7CFC00", "total": 6},
    {"id": "blue",   "name": "蓝色系", "color": "#87CEEB", "total": 6},
    {"id": "purple", "name": "紫色系", "color": "#8F00FF", "total": 5},
    {"id": "gray",   "name": "无彩色", "color": "#B2BEC3", "total": 4},
]

TOTAL_COLORS = 36

ALL_COLORS = [
    # 红色系
    {"id": "red_red",         "name": "正红",   "family": "red",    "rarity": "common"},
    {"id": "red_vermilion",   "name": "朱红",   "family": "red",    "rarity": "common"},
    {"id": "red_rose",        "name": "玫瑰红", "family": "red",    "rarity": "rare"},
    {"id": "red_burgundy",    "name": "酒红",   "family": "red",    "rarity": "rare"},
    {"id": "red_brick",       "name": "砖红",   "family": "red",    "rarity": "common"},
    {"id": "red_pink",        "name": "粉红",   "family": "red",    "rarity": "common"},
    # 橙色系
    {"id": "orange_orange",    "name": "橙",   "family": "orange", "rarity": "common"},
    {"id": "orange_tangerine", "name": "橘黄",  "family": "orange", "rarity": "common"},
    {"id": "orange_apricot",   "name": "杏色",  "family": "orange", "rarity": "rare"},
    {"id": "orange_amber",     "name": "琥珀",  "family": "orange", "rarity": "epic"},
    # 黄色系
    {"id": "yellow_bright",  "name": "明黄",  "family": "yellow", "rarity": "common"},
    {"id": "yellow_gold",    "name": "金黄",  "family": "yellow", "rarity": "epic"},
    {"id": "yellow_lemon",   "name": "柠檬黄", "family": "yellow", "rarity": "common"},
    {"id": "yellow_mustard", "name": "芥末黄", "family": "yellow", "rarity": "rare"},
    {"id": "yellow_cream",   "name": "米黄",  "family": "yellow", "rarity": "common"},
    # 绿色系
    {"id": "green_grass",   "name": "草绿",  "family": "green", "rarity": "common"},
    {"id": "green_emerald", "name": "翠绿",  "family": "green", "rarity": "rare"},
    {"id": "green_olive",   "name": "橄榄绿", "family": "green", "rarity": "common"},
    {"id": "green_mint",    "name": "薄荷绿", "family": "green", "rarity": "rare"},
    {"id": "green_dark",    "name": "墨绿",  "family": "green", "rarity": "epic"},
    {"id": "green_teal",    "name": "青绿",  "family": "green", "rarity": "rare"},
    # 蓝色系
    {"id": "blue_sky",    "name": "天蓝", "family": "blue", "rarity": "common"},
    {"id": "blue_lake",   "name": "湖蓝", "family": "blue", "rarity": "common"},
    {"id": "blue_navy",   "name": "海蓝", "family": "blue", "rarity": "epic"},
    {"id": "blue_indigo", "name": "靛蓝", "family": "blue", "rarity": "rare"},
    {"id": "blue_cobalt", "name": "钴蓝", "family": "blue", "rarity": "rare"},
    {"id": "blue_ice",    "name": "冰蓝", "family": "blue", "rarity": "common"},
    # 紫色系
    {"id": "purple_violet",   "name": "紫罗兰", "family": "purple", "rarity": "rare"},
    {"id": "purple_lavender", "name": "薰衣草", "family": "purple", "rarity": "common"},
    {"id": "purple_magenta",  "name": "品红",   "family": "purple", "rarity": "epic"},
    {"id": "purple_grape",    "name": "葡萄紫", "family": "purple", "rarity": "rare"},
    {"id": "purple_lilac",    "name": "淡紫",   "family": "purple", "rarity": "common"},
    # 无彩色
    {"id": "gray_black",  "name": "黑", "family": "gray", "rarity": "epic"},
    {"id": "gray_white",  "name": "白", "family": "gray", "rarity": "rare"},
    {"id": "gray_silver", "name": "银", "family": "gray", "rarity": "legendary"},
    {"id": "gray_gold",   "name": "金", "family": "gray", "rarity": "legendary"},
]


# 成就定义
ACHIEVEMENTS = [
    # 收集类
    {"id": "red",      "name": "红色狂热",   "desc": "集齐全部6种红色系颜色",   "icon": "🔴", "color": "#FF0000", "target": 6, "category": "collect"},
    {"id": "orange",   "name": "橙色收集家", "desc": "集齐全部4种橙色系颜色",   "icon": "🟠", "color": "#FFA500", "target": 4, "category": "collect"},
    {"id": "yellow",   "name": "黄色猎人",   "desc": "集齐全部5种黄色系颜色",   "icon": "🟡", "color": "#FFD700", "target": 5, "category": "collect"},
    {"id": "green",    "name": "绿色守护者", "desc": "集齐全部6种绿色系颜色",   "icon": "🟢", "color": "#7CFC00", "target": 6, "category": "collect"},
    {"id": "blue",     "name": "蓝色梦想家", "desc": "集齐全部6种蓝色系颜色",   "icon": "🔵", "color": "#87CEEB", "target": 6, "category": "collect"},
    {"id": "purple",   "name": "紫色神秘",   "desc": "集齐全部5种紫色系颜色",   "icon": "🟣", "color": "#8F00FF", "target": 5, "category": "collect"},
    {"id": "gray",     "name": "无彩大师",   "desc": "集齐全部4种无彩色/金属色", "icon": "⚪", "color": "#B2BEC3", "target": 4, "category": "collect"},
    {"id": "full",     "name": "全色谱大师", "desc": "集齐全部36种颜色",        "icon": "🌈", "color": "#FFD700", "target": 36, "category": "collect"},
    # 稀有度类
    {"id": "novice",   "name": "新手猎色",   "desc": "累计收集18种常见颜色", "icon": "⭐", "color": "#FFD700", "target": 18, "category": "rarity"},
    {"id": "rare",     "name": "稀有发现者", "desc": "累计收集11种稀有颜色", "icon": "✨", "color": "#74B9FF", "target": 11, "category": "rarity"},
    {"id": "epic",     "name": "史诗猎手",   "desc": "累计收集5种史诗颜色",  "icon": "💎", "color": "#A29BFE", "target": 5, "category": "rarity"},
    {"id": "legend",   "name": "传说之眼",   "desc": "累计收集2种传说颜色",  "icon": "👑", "color": "#FFD700", "target": 2, "category": "rarity"},
    # 特殊组合
    {"id": "primary",  "name": "三原色",   "desc": "集齐正红+明黄+天蓝",        "icon": "🎨", "color": "#00B894", "target": 3, "category": "combo"},
    {"id": "rainbow",  "name": "彩虹之路", "desc": "集齐红橙黄绿蓝靛紫7色",      "icon": "🌈", "color": "#00B894", "target": 7, "category": "combo"},
    {"id": "warmcool", "name": "冷暖对决", "desc": "同时拥有5种暖色+5种冷色",    "icon": "🔥", "color": "#00B894", "target": 10, "category": "combo"},
    {"id": "bw",       "name": "黑白之间", "desc": "集齐黑+白+银",               "icon": "⚫", "color": "#00B894", "target": 3, "category": "combo"},
    # 地点/时间
    {"id": "golden",   "name": "黄金时刻", "desc": "日落时收集到金色或橙色",      "icon": "🌅", "color": "#74B9FF", "target": 1, "category": "location"},
]

# 特殊组合成就的颜色 ID 匹配
COMBO_CHECKS = {
    "primary": ["red_red", "yellow_bright", "blue_sky"],
    "bw": ["gray_black", "gray_white", "gray_silver"],
}

# 暖色/冷色定义
WARM_COLORS = {"red", "orange", "yellow"}
COOL_COLORS = {"green", "blue", "purple"}

# 彩虹之路的 7 色
RAINBOW_COLORS = ["red_red", "orange_orange", "yellow_bright", "green_grass",
                   "blue_sky", "purple_violet", "purple_magenta"]


def _get_collected_ids(db: Session, user_id: str) -> list:
    """获取用户已收集的颜色 ID 列表"""
    record = db.query(UserCollection).filter(UserCollection.user_id == user_id).first()
    if record and record.collected_ids:
        return [c.strip() for c in record.collected_ids.split(",") if c.strip()]
    return []


def _count_by_rarity(collected_ids: list, rarity: str) -> int:
    return sum(1 for c in ALL_COLORS if c["id"] in collected_ids and c["rarity"] == rarity)


def _count_by_family(collected_ids: list, family: str) -> int:
    return sum(1 for c in ALL_COLORS if c["id"] in collected_ids and c["family"] == family)


def get_collection_progress(db: Session, user_id: str) -> dict:
    """获取收集进度"""
    collected_ids = _get_collected_ids(db, user_id)
    total_collected = len(collected_ids)

    families = []
    for f in COLOR_FAMILIES:
        collected = _count_by_family(collected_ids, f["id"])
        families.append({
            "id": f["id"],
            "name": f["name"],
            "color": f["color"],
            "collected": collected,
            "total": f["total"],
        })

    return {
        "total_colors": TOTAL_COLORS,
        "total_collected": total_collected,
        "percent": round(total_collected / TOTAL_COLORS * 100, 1) if TOTAL_COLORS else 0,
        "families": families,
    }


def get_user_collection(db: Session, user_id: str) -> dict:
    """获取用户已收集的颜色 ID 列表"""
    return {
        "collected_ids": _get_collected_ids(db, user_id),
    }


def _compute_achievement_progress(ach: dict, collected_ids: list) -> int:
    """计算单个成就的当前进度"""
    if ach["id"] in COMBO_CHECKS:
        return sum(1 for cid in COMBO_CHECKS[ach["id"]] if cid in collected_ids)
    if ach["id"] == "rainbow":
        return sum(1 for cid in RAINBOW_COLORS if cid in collected_ids)
    if ach["id"] == "warmcool":
        warm = sum(1 for c in ALL_COLORS if c["id"] in collected_ids and c["family"] in WARM_COLORS)
        cool = sum(1 for c in ALL_COLORS if c["id"] in collected_ids and c["family"] in COOL_COLORS)
        return min(10, warm + cool)
    if ach["id"] == "golden":
        return 1 if ("orange_orange" in collected_ids or "yellow_gold" in collected_ids) else 0
    if ach["id"] in ("novice", "rare", "epic", "legend"):
        rarity_map = {"novice": "common", "rare": "rare", "epic": "epic", "legend": "legendary"}
        return _count_by_rarity(collected_ids, rarity_map[ach["id"]])
    if ach["id"] == "full":
        return len(collected_ids)
    if ach["id"] == "gray":
        return _count_by_family(collected_ids, "gray")
    # 色系收集成就
    return _count_by_family(collected_ids, ach["id"])


def get_achievements(db: Session, user_id: str) -> dict:
    """获取成就列表及进度"""
    collected_ids = _get_collected_ids(db, user_id)

    list_data = []
    done = 0

    for ach in ACHIEVEMENTS:
        progress = _compute_achievement_progress(ach, collected_ids)
        unlocked = progress >= ach["target"]
        if unlocked:
            done += 1

        list_data.append({
            "id": ach["id"],
            "name": ach["name"],
            "desc": ach["desc"],
            "icon": ach["icon"],
            "color": ach["color"],
            "progress": progress,
            "target": ach["target"],
            "unlocked": unlocked,
            "category": ach["category"],
        })

    return {
        "total": len(ACHIEVEMENTS),
        "done": done,
        "list": list_data,
    }


def add_collected_color(db: Session, user_id: str, color_id: str) -> dict:
    """添加新收集的颜色，返回该颜色信息和断点判定的新成就"""
    # 校验颜色 ID 是否合法
    valid = any(c["id"] == color_id for c in ALL_COLORS)
    if not valid:
        return {"success": False, "is_new": False, "achievements_unlocked": []}

    record = db.query(UserCollection).filter(UserCollection.user_id == user_id).first()
    if not record:
        record = UserCollection(user_id=user_id, collected_ids="")
        db.add(record)

    old_ids = _get_collected_ids(db, user_id)

    # 跳过已收集的颜色
    if color_id in old_ids:
        return {"success": True, "is_new": False, "achievements_unlocked": []}

    new_ids = old_ids + [color_id]
    record.collected_ids = ",".join(new_ids)
    record.updated_at = datetime.utcnow()
    db.commit()

    # === 断点判定：对比新旧状态，找出刚解锁的成就 ===
    unlocked_now = []
    for ach in ACHIEVEMENTS:
        old_progress = _compute_achievement_progress(ach, old_ids)
        new_progress = _compute_achievement_progress(ach, new_ids)
        if old_progress < ach["target"] <= new_progress:
            unlocked_now.append({
                "id": ach["id"],
                "name": ach["name"],
                "icon": ach["icon"],
                "color": ach["color"],
                "category": ach["category"],
            })

    return {
        "success": True,
        "is_new": True,
        "color_id": color_id,
        "achievements_unlocked": unlocked_now,
    }

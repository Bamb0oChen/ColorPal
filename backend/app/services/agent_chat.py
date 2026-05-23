"""ColorPal 小彩对话服务。"""

import logging
from typing import Literal

import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.services.crud_photo import get_photo_list
from app.services.crud_task import get_current_task
from app.services.crud_user import get_profile

logger = logging.getLogger(__name__)

ChatSource = Literal['model', 'fallback']

SYSTEM_PROMPT = """你是 ColorPal 的色彩小人“小彩”。
你陪用户拍照收集颜色、理解色彩评分、照顾小人的能量成长。
回答必须使用中文，语气温暖、有一点灵动，但不要幼稚。
每次回复控制在 2-4 句，不要编造不存在的功能。
如果用户想拍照或上传照片，引导他点击“去拍照”。
不要要求用户在聊天里上传图片。"""

TIMEOUT = 8
MAX_HISTORY = 8


async def chat_with_agent(
    db: Session,
    message: str,
    history: list[dict],
    user_id: str = 'default',
) -> dict:
    """主路径：模型回复，失败则退到本地规则回复。"""
    context = _build_context(db, user_id)
    normalized_history = _normalize_history(history)

    try:
        reply = await _call_chat_model(message, normalized_history, context)
        return {
            'reply': reply,
            'quick_replies': _quick_replies(context),
            'source': 'model',
        }
    except Exception as err:
        logger.warning('Agent 模型失败，降级到规则回复: %s', err)
        return {
            'reply': _fallback_reply(message, context),
            'quick_replies': _quick_replies(context),
            'source': 'fallback',
        }


def _build_context(db: Session, user_id: str) -> dict:
    """把用户状态压成短上下文，避免把数据库结构暴露给模型。"""
    profile = get_profile(db, user_id)
    photos = get_photo_list(db, user_id, page=1, limit=5).get('photos', [])
    task = get_current_task(db, user_id)

    return {
        'profile': profile,
        'recent_photos': photos,
        'current_task': task,
    }


def _normalize_history(history: list[dict]) -> list[dict]:
    normalized = []
    for item in history[-MAX_HISTORY:]:
        role = item.get('role')
        content = str(item.get('content', '')).strip()
        if role not in {'user', 'assistant'} or not content:
            continue
        normalized.append({'role': role, 'content': content[:500]})
    return normalized


async def _call_chat_model(message: str, history: list[dict], context: dict) -> str:
    api_key = settings.chat_api_key or settings.vision_api_key
    api_base_url = settings.chat_api_base_url or settings.vision_api_base_url
    model = settings.chat_model or settings.vision_model

    if not api_key:
        raise ValueError('CHAT_API_KEY / VISION_API_KEY 未配置')

    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'system', 'content': _format_context(context)},
        *history,
        {'role': 'user', 'content': message[:1000]},
    ]

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            api_base_url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 280,
            },
        )
        resp.raise_for_status()
        content = resp.json()['choices'][0]['message']['content']
        return str(content).strip()[:800] or _fallback_reply(message, context)


def _format_context(context: dict) -> str:
    profile = context['profile']
    pet = profile['pet']
    energy = pet['energy']
    stats = profile['stats']
    task = context['current_task']
    photos = context['recent_photos']

    task_text = '暂无当前任务'
    if task:
        task_text = (
            f"{task['title']}：{task['description']}，"
            f"奖励 {task['reward_energy']} 能量"
        )

    photo_text = '暂无照片记录'
    if photos:
        photo_text = '；'.join(
            f"{p['dominant_color']} / {p['score']}分 / {p['comment']}" for p in photos
        )

    return f"""当前 ColorPal 上下文：
- 用户昵称：{profile['nickname']}
- 小人：{pet['name']}，心情 {pet['mood']}，主色 {pet['color']}，阶段 {pet['stage']}
- 能量：{energy['current']}/{energy['max']}，RGB=({energy['r']},{energy['g']},{energy['b']})
- 统计：已拍 {stats['total_photos']} 张，最高分 {stats['highest_score']}，
  连续 {stats['streak_days']} 天
- 当前任务：{task_text}
- 最近照片：{photo_text}"""


def _fallback_reply(message: str, context: dict) -> str:
    lowered = message.lower()
    profile = context['profile']
    pet = profile['pet']
    energy = pet['energy']
    task = context['current_task']
    photos = context['recent_photos']

    if any(word in lowered for word in ['任务', 'task', '拍什么', '挑战']):
        if task:
            return (
                f"今天可以先做「{task['title']}」：{task['description']}。"
                f"完成后我能吃到 {task['reward_energy']} 点能量，"
                "颜色会更有精神。"
            )
        return (
            '现在还没有新的任务。你可以先去拍一张最吸引你的颜色，'
            '我会按色彩搭配给你打分。'
        )

    if any(word in lowered for word in ['能量', '状态', '小彩', '心情', '成长']):
        return (
            f"我现在是 {pet['mood']} 状态，主色是 {pet['color']}，"
            f"能量 {energy['current']}/{energy['max']}。"
            "再收集几张有明确主色的照片，我的颜色会变得更鲜明。"
        )

    if any(word in lowered for word in ['照片', '拍照', '上传', '分析', '颜色']):
        return (
            '可以从一个颜色很明确的场景开始，'
            '比如夕阳、招牌、花束或一面有趣的墙。'
            '拍完后我会看主色、饱和度和明暗，再给它一个 0-100 的色彩分。'
        )

    if photos:
        latest = photos[0]
        return (
            f"上一张照片是 {latest['dominant_color']}，得了 {latest['score']} 分。"
            "如果你想冲高分，试试找一个主色清楚、"
            "背景干净、光线柔和的画面。"
        )

    return (
        '嗨，我是小彩。你拍到的颜色会变成我的能量，'
        '我也会帮你判断这张照片的配色是不是有意思。'
        '先去拍一张颜色最抓眼的东西吧。'
    )


def _quick_replies(context: dict) -> list[str]:
    replies = ['去拍照', '看看小彩状态']
    if context['current_task']:
        replies.insert(1, '今日任务')
    else:
        replies.insert(1, '拍什么好')
    return replies

"""AI 视觉分析服务（主路径调用 Qwen/DeepSeek，兜底走规则评分）。"""

import base64
import json
import logging
import re

import httpx

from app.config import settings
from app.services.scorer import fallback_score

logger = logging.getLogger(__name__)
HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$')
COLOR_CATEGORIES = {'warm', 'cool', 'neutral'}
LEVELS = {'high', 'medium', 'low'}

SYSTEM_PROMPT = """你是一位专业的色彩分析师。分析这张照片，只返回 JSON，不要额外文字。"""

USER_PROMPT = """分析这张照片的色彩，返回 JSON：
{
  "dominant_color": "#HEX",
  "palette": ["#HEX", ...],
  "score": 0-100,
  "comment": "中文评价（10-20字）",
  "color_category": "warm|cool|neutral",
  "saturation_level": "high|medium|low",
  "brightness_level": "high|medium|low"
}"""

TIMEOUT = 8


async def analyze_image(image_bytes: bytes) -> dict:
    """主路径：视觉模型分析，失败则降级到规则评分。"""
    try:
        return await _call_vision_model(image_bytes)
    except Exception as err:
        logger.warning('视觉模型失败，降级到规则评分: %s', err)
        return fallback_score(image_bytes)


async def _call_vision_model(image_bytes: bytes) -> dict:
    """调用 OpenAI-compatible 视觉模型接口。"""
    if not settings.vision_api_key:
        raise ValueError('VISION_API_KEY 未配置')

    b64 = base64.b64encode(image_bytes).decode()

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            settings.vision_api_base_url,
            headers={
                'Authorization': f'Bearer {settings.vision_api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': settings.vision_model,
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': USER_PROMPT},
                            {
                                'type': 'image_url',
                                'image_url': {'url': f'data:image/jpeg;base64,{b64}'},
                            },
                        ],
                    },
                ],
                'max_tokens': 500,
            },
        )
        resp.raise_for_status()
        content = resp.json()['choices'][0]['message']['content']
        return _validate(json.loads(content))


def _validate(data: dict) -> dict:
    """校验并修正 AI 返回结果。"""
    score = data.get('score', 50)
    if not isinstance(score, (int, float)):
        score = 50
    score = max(0, min(100, int(score)))

    dominant = data.get('dominant_color', '#CCCCCC')
    if not isinstance(dominant, str) or not HEX_RE.match(dominant):
        dominant = '#CCCCCC'

    palette = data.get('palette', [])
    if not isinstance(palette, list):
        palette = []
    palette = [color for color in palette if isinstance(color, str) and HEX_RE.match(color)][:5]

    color_category = data.get('color_category', 'neutral')
    if color_category not in COLOR_CATEGORIES:
        color_category = 'neutral'

    saturation_level = data.get('saturation_level', 'medium')
    if saturation_level not in LEVELS:
        saturation_level = 'medium'

    brightness_level = data.get('brightness_level', 'medium')
    if brightness_level not in LEVELS:
        brightness_level = 'medium'

    return {
        'dominant_color': dominant,
        'palette': palette,
        'score': score,
        'comment': str(data.get('comment', ''))[:50],
        'color_category': color_category,
        'saturation_level': saturation_level,
        'brightness_level': brightness_level,
    }

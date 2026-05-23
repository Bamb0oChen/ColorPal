"""AI 视觉分析服务（主路径调用 Qwen/DeepSeek，兜底走规则评分）。"""

import base64
import colorsys
import json
import logging
import re

import httpx

from app.config import settings
from app.services.scorer import extract_representative_palette, fallback_score

logger = logging.getLogger(__name__)
HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$')
COLOR_CATEGORIES = {'warm', 'cool', 'neutral'}
LEVELS = {'high', 'medium', 'low'}

SYSTEM_PROMPT = """你是一位专业视觉色彩分析师，为 ColorPal 选择照片代表色。
只返回严格 JSON，不要 Markdown，不要代码块，不要额外解释。"""

USER_PROMPT = """分析这张照片的色彩。请按 ColorPal 的产品语义选择颜色：

1. dominant_color 是“代表色/特征色/氛围色”，不是简单最大面积颜色。
2. 所有颜色必须来自图片真实可见像素，只能近似取色，不要为了配色好看而虚构颜色。
3. 忽略或降低这些元素权重：白色卡片/留白、黑灰文字、logo、二维码、水印、边框、分隔线。
4. 如果图片是海报、截图、卡片或带大面积文字，重点分析整体背景和插画/图形的主氛围色。
5. palette 返回 3-5 个互不重复的主要色，按视觉重要性排序。
   除非图片确实是黑白灰，否则不要让黑白灰占据前列。
6. score 评估色彩搭配、辨识度、饱和度、明暗平衡和整体美感，范围 0-100。
7. 不要返回模板色、品牌默认色或示例色。
   若蓝色、橙色、红色、紫色不在图片中清晰可见，不要把它们放入 palette。

返回 JSON：
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
                'temperature': 0.1,
            },
        )
        resp.raise_for_status()
        content = resp.json()['choices'][0]['message']['content']
        return _correct_with_local_palette(_validate(json.loads(content)), image_bytes)


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


def _correct_with_local_palette(data: dict, image_bytes: bytes) -> dict:
    """当模型颜色明显偏离真实像素时，用本地代表色校正。"""
    local_palette = extract_representative_palette(image_bytes)
    if not local_palette:
        return data

    model_colors = [data['dominant_color'], *data['palette']]
    close_count = sum(
        1
        for color in model_colors
        if any(_hex_distance(color, local) <= 72 for local in local_palette)
    )
    dominant_is_close = any(
        _hex_distance(data['dominant_color'], local) <= 72 for local in local_palette
    )

    if dominant_is_close and close_count >= max(1, len(model_colors) // 2):
        return data

    logger.warning(
        '模型颜色与本地像素差异较大，使用本地调色板校正: model=%s local=%s',
        model_colors,
        local_palette,
    )

    return {
        **data,
        'dominant_color': local_palette[0],
        'palette': local_palette,
        'comment': '画面明亮柔和，主色清新自然',
        'color_category': _color_category(local_palette[0]),
        'saturation_level': _saturation_level(local_palette[0]),
        'brightness_level': _brightness_level(local_palette[0]),
    }


def _hex_distance(left: str, right: str) -> float:
    left_rgb = _hex_to_rgb(left)
    right_rgb = _hex_to_rgb(right)
    return sum((l - r) ** 2 for l, r in zip(left_rgb, right_rgb)) ** 0.5


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    return tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))


def _color_category(hex_color: str) -> str:
    hue, _, saturation = _hex_to_hls(hex_color)
    if saturation < 0.16:
        return 'neutral'
    if hue < 35 / 360 or hue >= 330 / 360 or 35 / 360 <= hue < 75 / 360:
        return 'warm'
    return 'cool'


def _saturation_level(hex_color: str) -> str:
    _, _, saturation = _hex_to_hls(hex_color)
    if saturation >= 0.58:
        return 'high'
    if saturation >= 0.28:
        return 'medium'
    return 'low'


def _brightness_level(hex_color: str) -> str:
    _, lightness, _ = _hex_to_hls(hex_color)
    if lightness >= 0.68:
        return 'high'
    if lightness >= 0.36:
        return 'medium'
    return 'low'


def _hex_to_hls(hex_color: str) -> tuple[float, float, float]:
    r, g, b = (value / 255 for value in _hex_to_rgb(hex_color))
    return colorsys.rgb_to_hls(r, g, b)

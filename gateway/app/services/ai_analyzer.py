"""AI 视觉分析服务（主路径调用 GPT-4V，兜底走规则评分）"""

import json
import base64
import logging

import httpx
from app.config import settings
from app.services.scorer import fallback_score

logger = logging.getLogger(__name__)

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

TIMEOUT = 15


async def analyze_image(image_bytes: bytes) -> dict:
    """主路径：GPT-4V 分析，失败则降级到规则评分"""
    try:
        return await _call_gpt4v(image_bytes)
    except Exception as err:
        logger.warning("GPT-4V 失败，降级到规则评分: %s", err)
        return fallback_score(image_bytes)


async def _call_gpt4v(image_bytes: bytes) -> dict:
    """调用 OpenAI GPT-4V"""
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY 未配置")

    b64 = base64.b64encode(image_bytes).decode()

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": USER_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                            },
                        ],
                    },
                ],
                "max_tokens": 500,
            },
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return _validate(json.loads(content))


def _validate(data: dict) -> dict:
    """校验并修正 AI 返回结果"""
    score = data.get("score", 50)
    if not isinstance(score, (int, float)):
        score = 50
    score = max(0, min(100, int(score)))

    dominant = data.get("dominant_color", "#CCCCCC")
    if not isinstance(dominant, str) or not dominant.startswith("#"):
        dominant = "#CCCCCC"

    return {
        "dominant_color": dominant,
        "palette": data.get("palette", [])[:5],
        "score": score,
        "comment": data.get("comment", "")[:50],
        "color_category": data.get("color_category", "neutral"),
        "saturation_level": data.get("saturation_level", "medium"),
        "brightness_level": data.get("brightness_level", "medium"),
    }

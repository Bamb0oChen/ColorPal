"""规则评分引擎（GPT-4V 不可用时的兜底方案）"""

import io
import math
from PIL import Image
from collections import Counter


def fallback_score(image_bytes: bytes) -> dict:
    """
    基于颜色直方图的简单评分
    不使用 AI，纯图像处理
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pixels = list(img.getdata())

    # 饱和度评分
    total_s = 0
    for r, g, b in pixels:
        mx, mn = max(r, g, b), min(r, g, b)
        if mx == 0:
            s = 0
        else:
            s = (mx - mn) / mx
        total_s += s
    sat_score = (total_s / len(pixels)) * 100

    # 亮度评分（避让过暗/过亮）
    total_l = 0
    for r, g, b in pixels:
        l = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        total_l += l
    avg_l = total_l / len(pixels)
    # 亮度在 0.3-0.7 之间最佳
    brightness = 100 - min(abs(avg_l - 0.5) * 200, 100)

    # 色彩丰富度（缩放到 8x8 统计不同颜色数）
    small = img.resize((8, 8))
    quantized = [(r // 64, g // 64, b // 64) for r, g, b in small.getdata()]
    unique = len(Counter(quantized))
    variety = min(unique * 12, 100)

    score = int(sat_score * 0.4 + brightness * 0.3 + variety * 0.3)
    score = max(0, min(100, score))

    # 主色调（取最频繁的颜色）
    most_common = Counter(pixels).most_common(1)[0][0]
    dominant = "#{:02X}{:02X}{:02X}".format(*most_common)

    return {
        "dominant_color": dominant,
        "palette": [],
        "score": score,
        "comment": "色彩分析完成（规则评分）",
        "color_category": "neutral",
        "saturation_level": "high" if sat_score > 60 else "low",
        "brightness_level": "high" if avg_l > 0.6 else "low",
    }

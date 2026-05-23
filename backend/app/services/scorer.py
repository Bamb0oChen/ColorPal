"""规则评分引擎（视觉模型不可用时的兜底方案）"""

import colorsys
import io
from collections import Counter

from PIL import Image


def extract_representative_palette(image_bytes: bytes, limit: int = 5) -> list[str]:
    """提取避开白底、文字和灰阶噪声后的代表色。"""
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img.thumbnail((160, 160))

    weighted_colors: dict[tuple[int, int, int], float] = {}
    fallback_colors: Counter[tuple[int, int, int]] = Counter()

    for r, g, b in img.getdata():
        _, lightness, saturation = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        bucket = _quantize_rgb((r, g, b), step=16)
        fallback_colors[bucket] += 1

        if _is_low_signal_color(r, g, b, lightness, saturation):
            continue

        # 轻微偏好有色彩信息、亮度不过极端的区域，降低文字和留白影响。
        lightness_weight = max(0.35, 1 - abs(lightness - 0.62))
        weighted_colors[bucket] = (
            weighted_colors.get(bucket, 0) + (1 + saturation * 2) * lightness_weight
        )

    ranked_colors = (
        sorted(weighted_colors.items(), key=lambda item: item[1], reverse=True)
        if weighted_colors
        else fallback_colors.most_common()
    )

    selected: list[tuple[int, int, int]] = []
    for rgb, _ in ranked_colors:
        if all(_rgb_distance(rgb, existing) >= 34 for existing in selected):
            selected.append(rgb)
        if len(selected) >= limit:
            break

    return ['#{:02X}{:02X}{:02X}'.format(*rgb) for rgb in selected]

def fallback_score(image_bytes: bytes) -> dict:
    """
    基于颜色直方图的简单评分
    不使用 AI，纯图像处理
    """
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
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

    palette = extract_representative_palette(image_bytes)
    most_common = Counter(pixels).most_common(1)[0][0]
    dominant = palette[0] if palette else '#{:02X}{:02X}{:02X}'.format(*most_common)

    return {
        'dominant_color': dominant,
        'palette': palette,
        'score': score,
        'comment': '色彩分析完成（规则评分）',
        'color_category': _color_category(dominant),
        'saturation_level': 'high' if sat_score > 60 else 'low',
        'brightness_level': 'high' if avg_l > 0.6 else 'low',
    }


def _quantize_rgb(rgb: tuple[int, int, int], step: int) -> tuple[int, int, int]:
    return tuple(min(255, (value // step) * step + step // 2) for value in rgb)


def _is_low_signal_color(
    r: int,
    g: int,
    b: int,
    lightness: float,
    saturation: float,
) -> bool:
    if lightness < 0.14:
        return True
    if lightness > 0.86 and (saturation < 0.32 or min(r, g, b) > 228):
        return True
    return saturation < 0.1 and (lightness < 0.38 or lightness > 0.72)


def _rgb_distance(left: tuple[int, int, int], right: tuple[int, int, int]) -> float:
    return sum((l - r) ** 2 for l, r in zip(left, right)) ** 0.5


def _color_category(hex_color: str) -> str:
    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    hue, _, saturation = colorsys.rgb_to_hls(r, g, b)
    if saturation < 0.16:
        return 'neutral'
    if hue < 35 / 360 or hue >= 330 / 360 or 35 / 360 <= hue < 75 / 360:
        return 'warm'
    return 'cool'

/**
 * ColorPal 颜色系统常量定义
 *
 * 本文件由颜色系统设计文档自动生成。
 * 修改颜色数据请先修改 docs/配色方案.md，再同步到此文件。
 */

// ============================================================
// 1. 颜色稀有度定义
// ============================================================

export enum Rarity {
  COMMON = 'common',
  RARE = 'rare',
  EPIC = 'epic',
  LEGENDARY = 'legendary',
}

export const RarityLabel: Record<Rarity, string> = {
  [Rarity.COMMON]: '常见',
  [Rarity.RARE]: '稀有',
  [Rarity.EPIC]: '史诗',
  [Rarity.LEGENDARY]: '传说',
};

export const RarityColor: Record<Rarity, string> = {
  [Rarity.COMMON]: '#B2BEC3',
  [Rarity.RARE]: '#74B9FF',
  [Rarity.EPIC]: '#A29BFE',
  [Rarity.LEGENDARY]: '#FFD700',
};

export const RarityBorderColor: Record<Rarity, string> = {
  [Rarity.COMMON]: '#E0E0E0',
  [Rarity.RARE]: '#74B9FF',
  [Rarity.EPIC]: '#A29BFE',
  [Rarity.LEGENDARY]: '#FFD700',
};

/** 稀有度星标（用于色块右上角展示） */
export const RarityStars: Record<Rarity, string> = {
  [Rarity.COMMON]: '',
  [Rarity.RARE]: '★',
  [Rarity.EPIC]: '★★',
  [Rarity.LEGENDARY]: '★★★',
};

/** 稀有度排序权重（用于成就判定排序） */
export const RarityWeight: Record<Rarity, number> = {
  [Rarity.COMMON]: 1,
  [Rarity.RARE]: 2,
  [Rarity.EPIC]: 3,
  [Rarity.LEGENDARY]: 4,
};

// ============================================================
// 2. 色系定义
// ============================================================

export enum ColorFamily {
  RED = 'red',
  ORANGE = 'orange',
  YELLOW = 'yellow',
  GREEN = 'green',
  BLUE = 'blue',
  PURPLE = 'purple',
  GRAY = 'gray',
}

export const ColorFamilyLabel: Record<ColorFamily, string> = {
  [ColorFamily.RED]: '红色系',
  [ColorFamily.ORANGE]: '橙色系',
  [ColorFamily.YELLOW]: '黄色系',
  [ColorFamily.GREEN]: '绿色系',
  [ColorFamily.BLUE]: '蓝色系',
  [ColorFamily.PURPLE]: '紫色系',
  [ColorFamily.GRAY]: '无彩色',
};

export const ColorFamilyColor: Record<ColorFamily, string> = {
  [ColorFamily.RED]: '#FF0000',
  [ColorFamily.ORANGE]: '#FFA500',
  [ColorFamily.YELLOW]: '#FFD700',
  [ColorFamily.GREEN]: '#7CFC00',
  [ColorFamily.BLUE]: '#87CEEB',
  [ColorFamily.PURPLE]: '#8F00FF',
  [ColorFamily.GRAY]: '#B2BEC3',
};

// ============================================================
// 3. 36 色完整数据
// ============================================================

export interface ColorItem {
  /** 唯一 ID，格式：{family}_{english} */
  id: string
  /** 中文名 */
  name: string
  /** 英文标识 */
  english: string
  /** HEX 色值 */
  hex: string
  /** 所属色系 */
  family: ColorFamily
  /** 稀有度 */
  rarity: Rarity
}

export const ALL_COLORS: ColorItem[] = [
  // ---- 红色系 ----
  { id: 'red_red',         name: '正红',   english: 'Red',          hex: '#FF0000', family: ColorFamily.RED,    rarity: Rarity.COMMON },
  { id: 'red_vermilion',   name: '朱红',   english: 'Vermilion',    hex: '#E34234', family: ColorFamily.RED,    rarity: Rarity.COMMON },
  { id: 'red_rose',        name: '玫瑰红', english: 'Rose Red',     hex: '#FF007F', family: ColorFamily.RED,    rarity: Rarity.RARE },
  { id: 'red_burgundy',    name: '酒红',   english: 'Burgundy',     hex: '#800020', family: ColorFamily.RED,    rarity: Rarity.RARE },
  { id: 'red_brick',       name: '砖红',   english: 'Brick Red',    hex: '#CB4154', family: ColorFamily.RED,    rarity: Rarity.COMMON },
  { id: 'red_pink',        name: '粉红',   english: 'Pink',         hex: '#FFC0CB', family: ColorFamily.RED,    rarity: Rarity.COMMON },

  // ---- 橙色系 ----
  { id: 'orange_orange',     name: '橙',   english: 'Orange',       hex: '#FFA500', family: ColorFamily.ORANGE, rarity: Rarity.COMMON },
  { id: 'orange_tangerine',  name: '橘黄', english: 'Tangerine',    hex: '#F28500', family: ColorFamily.ORANGE, rarity: Rarity.COMMON },
  { id: 'orange_apricot',    name: '杏色', english: 'Apricot',      hex: '#FBCEB1', family: ColorFamily.ORANGE, rarity: Rarity.RARE },
  { id: 'orange_amber',      name: '琥珀', english: 'Amber',        hex: '#FFBF00', family: ColorFamily.ORANGE, rarity: Rarity.EPIC },

  // ---- 黄色系 ----
  { id: 'yellow_bright',   name: '明黄',   english: 'Bright Yellow', hex: '#FFFF00', family: ColorFamily.YELLOW, rarity: Rarity.COMMON },
  { id: 'yellow_gold',     name: '金黄',   english: 'Gold',          hex: '#FFD700', family: ColorFamily.YELLOW, rarity: Rarity.EPIC },
  { id: 'yellow_lemon',    name: '柠檬黄', english: 'Lemon',         hex: '#FFF700', family: ColorFamily.YELLOW, rarity: Rarity.COMMON },
  { id: 'yellow_mustard',  name: '芥末黄', english: 'Mustard',       hex: '#E1AD01', family: ColorFamily.YELLOW, rarity: Rarity.RARE },
  { id: 'yellow_cream',    name: '米黄',   english: 'Cream',         hex: '#FFFDD0', family: ColorFamily.YELLOW, rarity: Rarity.COMMON },

  // ---- 绿色系 ----
  { id: 'green_grass',    name: '草绿',   english: 'Grass Green', hex: '#7CFC00', family: ColorFamily.GREEN, rarity: Rarity.COMMON },
  { id: 'green_emerald',  name: '翠绿',   english: 'Emerald',     hex: '#50C878', family: ColorFamily.GREEN, rarity: Rarity.RARE },
  { id: 'green_olive',    name: '橄榄绿', english: 'Olive',       hex: '#808000', family: ColorFamily.GREEN, rarity: Rarity.COMMON },
  { id: 'green_mint',     name: '薄荷绿', english: 'Mint',        hex: '#98FB98', family: ColorFamily.GREEN, rarity: Rarity.RARE },
  { id: 'green_dark',     name: '墨绿',   english: 'Dark Green',  hex: '#004d00', family: ColorFamily.GREEN, rarity: Rarity.EPIC },
  { id: 'green_teal',     name: '青绿',   english: 'Teal',        hex: '#008080', family: ColorFamily.GREEN, rarity: Rarity.RARE },

  // ---- 蓝色系 ----
  { id: 'blue_sky',    name: '天蓝',   english: 'Sky Blue',  hex: '#87CEEB', family: ColorFamily.BLUE, rarity: Rarity.COMMON },
  { id: 'blue_lake',   name: '湖蓝',   english: 'Lake Blue', hex: '#30D5C8', family: ColorFamily.BLUE, rarity: Rarity.COMMON },
  { id: 'blue_navy',   name: '海蓝',   english: 'Navy Blue', hex: '#000080', family: ColorFamily.BLUE, rarity: Rarity.EPIC },
  { id: 'blue_indigo', name: '靛蓝',   english: 'Indigo',    hex: '#4B0082', family: ColorFamily.BLUE, rarity: Rarity.RARE },
  { id: 'blue_cobalt', name: '钴蓝',   english: 'Cobalt',    hex: '#0047AB', family: ColorFamily.BLUE, rarity: Rarity.RARE },
  { id: 'blue_ice',    name: '冰蓝',   english: 'Ice Blue',  hex: '#E0F0FF', family: ColorFamily.BLUE, rarity: Rarity.COMMON },

  // ---- 紫色系 ----
  { id: 'purple_violet',    name: '紫罗兰', english: 'Violet',    hex: '#8F00FF', family: ColorFamily.PURPLE, rarity: Rarity.RARE },
  { id: 'purple_lavender',  name: '薰衣草', english: 'Lavender',  hex: '#E6E6FA', family: ColorFamily.PURPLE, rarity: Rarity.COMMON },
  { id: 'purple_magenta',   name: '品红',   english: 'Magenta',   hex: '#FF00FF', family: ColorFamily.PURPLE, rarity: Rarity.EPIC },
  { id: 'purple_grape',     name: '葡萄紫', english: 'Grape',      hex: '#6F2DA8', family: ColorFamily.PURPLE, rarity: Rarity.RARE },
  { id: 'purple_lilac',     name: '淡紫',   english: 'Lilac',      hex: '#C8A2C8', family: ColorFamily.PURPLE, rarity: Rarity.COMMON },

  // ---- 无彩色 ----
  { id: 'gray_black',  name: '黑', english: 'Black',         hex: '#000000', family: ColorFamily.GRAY, rarity: Rarity.EPIC },
  { id: 'gray_white',  name: '白', english: 'White',         hex: '#FFFFFF', family: ColorFamily.GRAY, rarity: Rarity.RARE },
  { id: 'gray_silver', name: '银', english: 'Silver',        hex: '#C0C0C0', family: ColorFamily.GRAY, rarity: Rarity.LEGENDARY },
  { id: 'gray_gold',   name: '金', english: 'Gold Metallic', hex: '#FFD700', family: ColorFamily.GRAY, rarity: Rarity.LEGENDARY },
];

// ============================================================
// 4. 工具函数
// ============================================================

/** 按 ID 查找颜色 */
export function getColorById(id: string): ColorItem | undefined {
  return ALL_COLORS.find((c) => c.id === id);
}

/** 按色值查找最近的颜色 */
export function findClosestColor(hex: string): ColorItem | undefined {
  const target = hexToRgb(hex);
  if (!target) return undefined;
  const targetHsl = rgbToHsl(target.r, target.g, target.b);

  let closest: ColorItem | undefined;
  let minDist = Infinity;

  for (const color of ALL_COLORS) {
    const rgb = hexToRgb(color.hex);
    if (!rgb) continue;
    if (target.r === rgb.r && target.g === rgb.g && target.b === rgb.b) return color;

    const colorHsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
    const hueDist = hueDistance(targetHsl.h, colorHsl.h) / 180;
    const satDist = Math.abs(targetHsl.s - colorHsl.s);
    const lightDist = Math.abs(targetHsl.l - colorHsl.l);
    const rgbDist = colorDistance(target, rgb) / 441.68;
    let dist = hueDist * 3 + satDist * 0.85 + lightDist * 0.55 + rgbDist * 0.35;
    const targetFamily = inferColorFamily(targetHsl.h, targetHsl.s);

    if (targetHsl.s > 0.16 && color.family === ColorFamily.GRAY) {
      dist += 1.2;
    }
    if (targetHsl.s < 0.12 && color.family !== ColorFamily.GRAY) {
      dist += 0.5;
    }
    if (targetFamily && color.family !== targetFamily) {
      dist += 0.22;
    }

    if (dist < minDist) {
      minDist = dist;
      closest = color;
    }
  }

  return closest;
}

/** 按色系筛选颜色 */
export function getColorsByFamily(family: ColorFamily): ColorItem[] {
  return ALL_COLORS.filter((c) => c.family === family);
}

/** 按稀有度筛选颜色 */
export function getColorsByRarity(rarity: Rarity): ColorItem[] {
  return ALL_COLORS.filter((c) => c.rarity === rarity);
}

/** 获取色系收集进度 */
export function getFamilyProgress(
  collectedIds: string[],
  family: ColorFamily,
): { collected: number; total: number } {
  const familyColors = getColorsByFamily(family);
  const collected = familyColors.filter((c) => collectedIds.includes(c.id)).length;
  return { collected, total: familyColors.length };
}

/** 获取全局收集进度 */
export function getGlobalProgress(collectedIds: string[]): {
  collected: number;
  total: number;
  common: { collected: number; total: number };
  rare: { collected: number; total: number };
  epic: { collected: number; total: number };
  legendary: { collected: number; total: number };
} {
  return {
    collected: collectedIds.length,
    total: ALL_COLORS.length,
    common: {
      collected: allByRarity(Rarity.COMMON).filter((c) => collectedIds.includes(c.id)).length,
      total: allByRarity(Rarity.COMMON).length,
    },
    rare: {
      collected: allByRarity(Rarity.RARE).filter((c) => collectedIds.includes(c.id)).length,
      total: allByRarity(Rarity.RARE).length,
    },
    epic: {
      collected: allByRarity(Rarity.EPIC).filter((c) => collectedIds.includes(c.id)).length,
      total: allByRarity(Rarity.EPIC).length,
    },
    legendary: {
      collected: allByRarity(Rarity.LEGENDARY).filter((c) => collectedIds.includes(c.id)).length,
      total: allByRarity(Rarity.LEGENDARY).length,
    },
  };
}

function allByRarity(rarity: Rarity): ColorItem[] {
  return ALL_COLORS.filter((c) => c.rarity === rarity);
}

// ============================================================
// 5. 色彩工具函数
// ============================================================

function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

/** 计算两个 RGB 颜色的欧几里得距离（色距） */
function colorDistance(
  a: { r: number; g: number; b: number },
  b: { r: number; g: number; b: number },
): number {
  return Math.sqrt((a.r - b.r) ** 2 + (a.g - b.g) ** 2 + (a.b - b.b) ** 2);
}

function rgbToHsl(
  r: number,
  g: number,
  b: number,
): { h: number; s: number; l: number } {
  const red = r / 255;
  const green = g / 255;
  const blue = b / 255;
  const max = Math.max(red, green, blue);
  const min = Math.min(red, green, blue);
  const l = (max + min) / 2;

  if (max === min) return { h: 0, s: 0, l };

  const delta = max - min;
  const s = l > 0.5 ? delta / (2 - max - min) : delta / (max + min);
  let h = 0;

  if (max === red) {
    h = (green - blue) / delta + (green < blue ? 6 : 0);
  } else if (max === green) {
    h = (blue - red) / delta + 2;
  } else {
    h = (red - green) / delta + 4;
  }

  return { h: h * 60, s, l };
}

function hueDistance(left: number, right: number): number {
  const distance = Math.abs(left - right) % 360;
  return Math.min(distance, 360 - distance);
}

function inferColorFamily(hue: number, saturation: number): ColorFamily | null {
  if (saturation < 0.12) return ColorFamily.GRAY;
  if (hue < 15 || hue >= 330) return ColorFamily.RED;
  if (hue < 45) return ColorFamily.ORANGE;
  if (hue < 70) return ColorFamily.YELLOW;
  if (hue < 170) return ColorFamily.GREEN;
  if (hue < 255) return ColorFamily.BLUE;
  if (hue < 330) return ColorFamily.PURPLE;
  return null;
}

// ============================================================
// 6. 成就系统定义
// ============================================================

export enum AchievementCategory {
  COLLECT = 'collect',
  RARITY = 'rarity',
  COMBO = 'combo',
  LOCATION = 'location',
}

export const AchievementCategoryLabel: Record<AchievementCategory, string> = {
  [AchievementCategory.COLLECT]: '收集类',
  [AchievementCategory.RARITY]: '稀有度类',
  [AchievementCategory.COMBO]: '特殊组合',
  [AchievementCategory.LOCATION]: '地点/时间',
};

export const AchievementCategoryColor: Record<AchievementCategory, string> = {
  [AchievementCategory.COLLECT]: '#6C5CE7',
  [AchievementCategory.RARITY]: '#FFD700',
  [AchievementCategory.COMBO]: '#00B894',
  [AchievementCategory.LOCATION]: '#74B9FF',
};

export interface Achievement {
  id: string
  name: string
  description: string
  category: AchievementCategory
  /** 判定条件：检查收集的颜色 ID 列表是否满足此成就 */
  check?: (collectedIds: string[]) => boolean
  /** 成就标识色 */
  color: string
  /** 展示色值：单色 hex 或 CSS 渐变，用于成就卡片左侧色块 */
  swatch?: string
}

/** 内置成就列表 */
export function checkAchievements(collectedIds: string[]): Achievement[] {
  return ALL_ACHIEVEMENTS.filter((a) => a.check?.(collectedIds) && !a.check?.([]));
}

// 收集类辅助函数
function allInFamily(collectedIds: string[], family: ColorFamily): boolean {
  const familyColors = ALL_COLORS.filter((c) => c.family === family)
  return familyColors.every((c) => collectedIds.includes(c.id))
}

function countByRarity(collectedIds: string[], rarity: Rarity): number {
  return ALL_COLORS.filter((c) => c.rarity === rarity && collectedIds.includes(c.id)).length
}

export const ALL_ACHIEVEMENTS: Achievement[] = [
  // ---- 收集类 ----
  {
    id: 'achieve_red_fever', name: '红色狂热', description: '集齐全部 6 种红色系颜色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: '#FF0000',
    check: (ids) => allInFamily(ids, ColorFamily.RED),
  },
  {
    id: 'achieve_orange_collector', name: '橙色收集家', description: '集齐全部 4 种橙色系颜色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: '#FFA500',
    check: (ids) => allInFamily(ids, ColorFamily.ORANGE),
  },
  {
    id: 'achieve_yellow_hunter', name: '黄色猎人', description: '集齐全部 5 种黄色系颜色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: '#FFD700',
    check: (ids) => allInFamily(ids, ColorFamily.YELLOW),
  },
  {
    id: 'achieve_green_guardian', name: '绿色守护者', description: '集齐全部 6 种绿色系颜色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: '#7CFC00',
    check: (ids) => allInFamily(ids, ColorFamily.GREEN),
  },
  {
    id: 'achieve_blue_dreamer', name: '蓝色梦想家', description: '集齐全部 6 种蓝色系颜色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: '#87CEEB',
    check: (ids) => allInFamily(ids, ColorFamily.BLUE),
  },
  {
    id: 'achieve_purple_mystery', name: '紫色神秘', description: '集齐全部 5 种紫色系颜色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: '#8F00FF',
    check: (ids) => allInFamily(ids, ColorFamily.PURPLE),
  },
  {
    id: 'achieve_gray_master', name: '无彩大师', description: '集齐全部 4 种无彩色/金属色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: '#C0C0C0',
    check: (ids) => allInFamily(ids, ColorFamily.GRAY),
  },
  {
    id: 'achieve_full_spectrum', name: '全色谱大师', description: '集齐全部 36 种颜色',
    category: AchievementCategory.COLLECT, color: '#6C5CE7', swatch: 'linear-gradient(90deg, #FF0000, #FFA500, #FFD700, #7CFC00, #87CEEB, #8F00FF)',
    check: (ids) => ALL_COLORS.every((c) => ids.includes(c.id)),
  },
  // ---- 稀有度类 ----
  {
    id: 'achieve_novice', name: '新手猎色', description: '累计收集 18 种常见颜色',
    category: AchievementCategory.RARITY, color: '#FFD700', swatch: '#B2BEC3',
    check: (ids) => countByRarity(ids, Rarity.COMMON) >= 18,
  },
  {
    id: 'achieve_rare_finder', name: '稀有发现者', description: '累计收集 11 种稀有颜色',
    category: AchievementCategory.RARITY, color: '#FFD700', swatch: '#74B9FF',
    check: (ids) => countByRarity(ids, Rarity.RARE) >= 11,
  },
  {
    id: 'achieve_epic_hunter', name: '史诗猎手', description: '累计收集 5 种史诗颜色',
    category: AchievementCategory.RARITY, color: '#FFD700', swatch: '#A29BFE',
    check: (ids) => countByRarity(ids, Rarity.EPIC) >= 5,
  },
  {
    id: 'achieve_legend_eye', name: '传说之眼', description: '累计收集 2 种传说颜色',
    category: AchievementCategory.RARITY, color: '#FFD700', swatch: '#FFD700',
    check: (ids) => countByRarity(ids, Rarity.LEGENDARY) >= 2,
  },
  // ---- 特殊组合 ----
  {
    id: 'achieve_primary', name: '三原色', description: '集齐正红 + 明黄 + 天蓝',
    category: AchievementCategory.COMBO, color: '#00B894', swatch: 'linear-gradient(135deg, #FF0000 33%, #FFD700 33%, #FFD700 66%, #87CEEB 66%)',
    check: (ids) => ['red_red', 'yellow_bright', 'blue_sky'].every((id) => ids.includes(id)),
  },
  {
    id: 'achieve_rainbow', name: '彩虹之路', description: '集齐红橙黄绿蓝靛紫 7 色',
    category: AchievementCategory.COMBO, color: '#00B894', swatch: 'linear-gradient(90deg, #FF0000, #FFA500, #FFD700, #7CFC00, #87CEEB, #4B0082, #8F00FF)',
    check: (ids) => {
      const families = [ColorFamily.RED, ColorFamily.ORANGE, ColorFamily.YELLOW, ColorFamily.GREEN, ColorFamily.BLUE, ColorFamily.PURPLE]
      return families.every((f) => ALL_COLORS.some((c) => c.family === f && ids.includes(c.id)))
    },
  },
  {
    id: 'achieve_warm_cool', name: '冷暖对决', description: '同时拥有 5 种暖色 + 5 种冷色',
    category: AchievementCategory.COMBO, color: '#00B894', swatch: 'linear-gradient(135deg, #FF6B6B 50%, #74B9FF 50%)',
    check: (ids) => {
      const warm = ids.filter((id) => {
        const c = ALL_COLORS.find((x) => x.id === id)
        return c && [ColorFamily.RED, ColorFamily.ORANGE, ColorFamily.YELLOW].includes(c.family)
      }).length
      const cool = ids.filter((id) => {
        const c = ALL_COLORS.find((x) => x.id === id)
        return c && [ColorFamily.GREEN, ColorFamily.BLUE, ColorFamily.PURPLE].includes(c.family)
      }).length
      return warm >= 5 && cool >= 5
    },
  },
  {
    id: 'achieve_black_white', name: '黑白之间', description: '集齐黑 + 白 + 银',
    category: AchievementCategory.COMBO, color: '#00B894', swatch: 'linear-gradient(135deg, #000000 33%, #FFFFFF 33%, #FFFFFF 66%, #C0C0C0 66%)',
    check: (ids) => ['gray_black', 'gray_white', 'gray_silver'].every((id) => ids.includes(id)),
  },
];

// ============================================================
// 5. 精灵阶段经验值系统
// ============================================================

/** 每级所需累计经验值（索引 = 阶段） */
export const STAGE_XP_THRESHOLDS = [0, 200, 500, 1000, 2000, 5000, 10000]

/** 最大阶段（6，对应 10000+ XP） */
export const MAX_STAGE = STAGE_XP_THRESHOLDS.length - 1

/** 根据累计经验值计算阶段 */
export function getStageFromXP(totalEnergy: number): number {
  let stage = 0
  for (let i = STAGE_XP_THRESHOLDS.length - 1; i >= 0; i--) {
    if (totalEnergy >= STAGE_XP_THRESHOLDS[i]) {
      stage = i
      break
    }
  }
  return Math.min(stage, MAX_STAGE)
}

/** 当前阶段的下一阶段所需经验值 */
export function getStageXPProgress(totalEnergy: number): {
  stage: number
  currentXP: number
  nextStageXP: number
  progressPercent: number
} {
  const stage = getStageFromXP(totalEnergy)
  const currentThreshold = STAGE_XP_THRESHOLDS[stage]
  const nextThreshold = STAGE_XP_THRESHOLDS[Math.min(stage + 1, MAX_STAGE)]
  const xpInStage = totalEnergy - currentThreshold
  const xpNeeded = nextThreshold - currentThreshold
  const progressPercent = Math.min(Math.round((xpInStage / xpNeeded) * 100), 100)

  return { stage, currentXP: totalEnergy, nextStageXP: nextThreshold, progressPercent }
}

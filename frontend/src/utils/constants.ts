// 小人形态配置
export const PET_STAGES = [
  { level: 0, name: '幼年', energyRequired: 0 },
  { level: 1, name: '成长', energyRequired: 200 },
  { level: 2, name: '成熟', energyRequired: 500 },
  { level: 3, name: '稀有', energyRequired: 1000 },
]

// 评分阈值
export const SCORE_THRESHOLD = {
  HIGH: 70,
  MEDIUM: 40,
}

// 颜色分类
export const COLOR_CATEGORIES = {
  warm: '暖色调',
  cool: '冷色调',
  neutral: '中性色',
} as const

// API 路径
export const API = {
  PHOTO_ANALYZE: '/photo/analyze',
  USER_PROFILE: '/user/profile',
  TASK_CURRENT: '/task/current',
  COLLECTIONS: '/collections',
  MAP_POINTS: '/photos/map-points',
} as const

/**
 * ColorPal 颜色系统类型定义
 *
 * 与后端 API 返回的数据结构对齐。
 * 前端开发直接使用此类型定义。
 */

// ============================================================
// 颜色系统类型
// ============================================================

/** 稀有度枚举 */
export type Rarity = 'common' | 'rare' | 'epic' | 'legendary'

/** 色系枚举 */
export type ColorFamily = 'red' | 'orange' | 'yellow' | 'green' | 'blue' | 'purple' | 'gray'

/** 色温类别 */
export type ColorCategory = 'warm' | 'cool' | 'neutral'

/** 饱和度等级 */
export type SaturationLevel = 'high' | 'medium' | 'low'

/** 亮度等级 */
export type BrightnessLevel = 'high' | 'medium' | 'low'

/** 36 色标准色项 */
export interface ColorItem {
  id: string        // 如 "red_pink"
  name: string      // 中文名，如 "粉红"
  english: string   // 英文名，如 "Pink"
  hex: string       // 色值，如 "#FFC0CB"
  family: ColorFamily
  rarity: Rarity
}

// ============================================================
// API 响应类型
// ============================================================

/** 后端统一响应包装 */
export interface ApiResponse<T> {
  code: number
  data: T
  message: string
}

/** AI 分析结果 */
export interface AnalysisResult {
  dominant_color: string
  palette: string[]
  color_id?: string
  color_name?: string
  rarity?: Rarity
  score: number
  comment: string
  color_category: ColorCategory
  saturation_level: SaturationLevel
  brightness_level: BrightnessLevel
}

/** 能量变化 */
export interface EnergyChange {
  r: number
  g: number
  b: number
  total: number
  pet_mood?: 'happy' | 'neutral' | 'sad'
}

/** 照片分析响应 data 载荷 */
export interface PhotoAnalyzeData {
  photo_id: string
  analysis: AnalysisResult
  energy_change: EnergyChange
  task_completed: string | null
  achievements_unlocked?: string[]
}

/** 上传照片原始响应 */
export type UploadResponse = ApiResponse<PhotoAnalyzeData>

// ============================================================
// 收集与成就类型
// ============================================================

/** 色系收集进度 */
export interface FamilyProgress {
  family: ColorFamily
  label: string
  collected: number
  total: number
}

/** 全局收集进度 */
export interface GlobalProgress {
  total_collected: number
  total_all: number
  by_rarity: {
    common: { collected: number; total: number }
    rare: { collected: number; total: number }
    epic: { collected: number; total: number }
    legendary: { collected: number; total: number }
  }
  by_family: FamilyProgress[]
}

/** 成就分类 */
export type AchievementCategory = 'collect' | 'rarity' | 'combo' | 'location'

/** 成就项 */
export interface Achievement {
  id: string
  name: string
  description: string
  category: AchievementCategory
  progress: { current: number; target: number }
  unlocked: boolean
  unlocked_at?: string
}

/** 新颜色收集弹窗数据 */
export interface NewColorDiscovery {
  color: ColorItem
  is_new: boolean
  achievements_unlocked: Achievement[]
}

// ============================================================
// 小人状态类型
// ============================================================

/** 小人情绪 */
export type PetMood = 'happy' | 'neutral' | 'sad'

/** 小人进化阶段 */
export type PetStage = 0 | 1 | 2 | 3  // 0=幼年, 1=成体, 2=成熟, 3=稀有

/** 小人完整状态 */
export interface PetState {
  name: string
  stage: PetStage
  mood: PetMood
  color: string          // 当前主色调
  energy: {
    current: number
    max: number
    r: number
    g: number
    b: number
  }
}

// ============================================================
// 任务系统类型
// ============================================================

export type TaskType = 'color_collect' | 'combo' | 'streak' | 'location' | 'time' | 'community'

export interface Task {
  id: string
  type: TaskType
  title: string
  description: string
  target_color?: string
  target_category?: ColorCategory
  reward: {
    energy_bonus: number
  }
  status: 'active' | 'completed' | 'expired'
}

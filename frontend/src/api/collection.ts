import http from './request'

/** 色系收集进度 */
export interface FamilyProgress {
  id: string
  name: string
  color: string
  collected: number
  total: number
}

/** 收集总进度 */
export interface CollectionProgress {
  total_colors: number
  total_collected: number
  percent: number
  families: FamilyProgress[]
}

/** 成就项（后端返回格式） */
export interface AchievementDto {
  id: string
  name: string
  desc: string
  icon: string
  color: string
  progress: number
  target: number
  unlocked: boolean
  category?: string
}

/** 成就列表响应 */
export interface AchievementList {
  total: number
  done: number
  list: AchievementDto[]
}

/** 用户收集的颜色 ID 列表 */
export interface UserCollection {
  collected_ids: string[]
}

/** 获取收集进度 */
export const getCollectionProgress = async (): Promise<CollectionProgress> => {
  return http.get('/collections/progress')
}

/** 获取成就列表 */
export const getAchievements = async (): Promise<AchievementList> => {
  return http.get('/collections/achievements')
}

/** 获取用户已收集的颜色列表 */
export const getUserCollection = async (): Promise<UserCollection> => {
  return http.get('/collections/user')
}

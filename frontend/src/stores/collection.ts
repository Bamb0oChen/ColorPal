import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getCollectionProgress,
  getAchievements,
  getUserCollection,
} from '@/api/collection'
import type {
  CollectionProgress,
  AchievementDto,
  FamilyProgress,
} from '@/api/collection'
import { ALL_COLORS, ColorFamily, Rarity } from '@/utils/constants'
import type { ColorItem } from '@/utils/constants'
import type { ColorFamily as ColorFamilyType } from '@/types/photo'

export const useCollectionStore = defineStore('collection', () => {
  // ====== State ======
  const progress = ref<CollectionProgress | null>(null)
  const achievements = ref<AchievementDto[]>([])
  const collectedIds = ref<string[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // ====== Computed ======
  const totalColors = computed(() => ALL_COLORS.length)

  const totalCollected = computed(() => collectedIds.value.length)

  const collectPercent = computed(() =>
    totalColors.value > 0
      ? Math.round((totalCollected.value / totalColors.value) * 100)
      : 0,
  )

  /** 按色系分组的颜色列表 */
  const colorsByFamily = computed(() => {
    const map = new Map<string, ColorItem[]>()
    for (const family of Object.values(ColorFamily)) {
      map.set(
        family,
        ALL_COLORS.filter((c) => c.family === family),
      )
    }
    return map
  })

  /** 每个色系的收集进度 */
  const familyProgressMap = computed(() => {
    const map = new Map<string, { collected: number; total: number }>()
    for (const [family, colors] of colorsByFamily.value) {
      const collected = colors.filter((c) => collectedIds.value.includes(c.id)).length
      map.set(family, { collected, total: colors.length })
    }
    return map
  })

  /** 收集类成就完成数 */
  const doneAchievements = computed(() =>
    achievements.value.filter((a) => a.unlocked).length,
  )

  /** 总成就数 */
  const totalAchievements = computed(() => achievements.value.length)

  /** 按颜色 ID 判断是否已收集 */
  const isCollected = (colorId: string) => collectedIds.value.includes(colorId)

  // ====== Actions ======
  const fetchAll = async () => {
    isLoading.value = true
    error.value = null
    try {
      const [prog, ach, col] = await Promise.all([
        getCollectionProgress(),
        getAchievements(),
        getUserCollection(),
      ])
      progress.value = (prog as any).data
      achievements.value = (ach as any).data?.list ?? []
      collectedIds.value = (col as any).data?.collected_ids ?? []
    } catch (err: any) {
      error.value = err?.message || '获取收集数据失败'
      console.error('[CollectionStore]', error.value)
    } finally {
      isLoading.value = false
    }
  }

  /** 获取某个颜色的详细信息（供详情弹窗使用） */
  const getColorDetail = (colorId: string): ColorItem | undefined => {
    return ALL_COLORS.find((c) => c.id === colorId)
  }

  /** 获取某个色系的收集进度 */
  const getFamilyProgress = (family: ColorFamilyType) => {
    return familyProgressMap.value.get(family) ?? { collected: 0, total: 0 }
  }

  return {
    // state
    progress,
    achievements,
    collectedIds,
    isLoading,
    error,
    // computed
    totalColors,
    totalCollected,
    collectPercent,
    colorsByFamily,
    familyProgressMap,
    doneAchievements,
    totalAchievements,
    // actions
    fetchAll,
    isCollected,
    getColorDetail,
    getFamilyProgress,
  }
})

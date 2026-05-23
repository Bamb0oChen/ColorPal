import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { findClosestColor, getColorById, type ColorItem } from '@/utils/constants'

const STORAGE_KEY = 'colorpal.palette'
const NEW_KEY = 'colorpal.newly_unlocked'
const DEFAULT_COLORS = ['#ff6b6b', '#4ecdc4', '#ffe66d']

export const usePaletteStore = defineStore('palette', () => {
  const collectedColors = ref<string[]>(loadColors())
  const newlyUnlockedIds = ref<string[]>(loadNewlyUnlocked())

  const accentColor = computed(() => collectedColors.value[0] || DEFAULT_COLORS[0])

  const collectedColorItems = computed(() => {
    const seen = new Set<string>()
    return collectedColors.value
      .map((color) => findClosestColor(color))
      .filter((color): color is ColorItem => {
        if (!color || seen.has(color.id)) return false
        seen.add(color.id)
        return true
      })
  })

  const collectedIds = computed(() => new Set(collectedColorItems.value.map((c) => c.id)))

  const addColorFromImageName = (fileName: string) => {
    const next = colorFromText(fileName)
    addColor(next)
  }

  /** 按色值命中解锁（AI 分析返回 hex 时用） */
  function addColor(hex: string) {
    const match = findClosestColor(hex)
    const colorHex = match?.hex || hex
    collectedColors.value = [colorHex, ...collectedColors.value.filter((c) => c !== colorHex)].slice(0, 8)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectedColors.value))

    if (match && !collectedIds.value.has(match.id)) {
      if (!newlyUnlockedIds.value.includes(match.id)) {
        newlyUnlockedIds.value.push(match.id)
        saveNewlyUnlocked(newlyUnlockedIds.value)
      }
    }
  }

  /** 按色码 ID 直接解锁（Homepage AI 返回 colorId 时用） */
  function unlockColorById(colorId: string) {
    if (collectedIds.value.has(colorId)) return
    const match = getColorById(colorId)
    if (!match) return

    collectedColors.value = [match.hex, ...collectedColors.value.filter((c) => c !== match.hex)].slice(0, 8)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectedColors.value))

    if (!newlyUnlockedIds.value.includes(match.id)) {
      newlyUnlockedIds.value.push(match.id)
      saveNewlyUnlocked(newlyUnlockedIds.value)
    }
  }

  /** 清除新解锁标记（用户在图鉴页已查看） */
  function clearNewlyUnlocked() {
    newlyUnlockedIds.value = []
    localStorage.setItem(NEW_KEY, '[]')
  }

  /** 检查某个颜色 ID 是否刚解锁 */
  function isNewlyUnlocked(colorId: string): boolean {
    return newlyUnlockedIds.value.includes(colorId)
  }

  return {
    collectedColors,
    collectedColorItems,
    collectedIds,
    accentColor,
    newlyUnlockedIds,
    addColorFromImageName,
    addColor,
    unlockColorById,
    clearNewlyUnlocked,
    isNewlyUnlocked,
  }
})

function loadColors(): string[] {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return DEFAULT_COLORS
  try {
    const colors = JSON.parse(raw) as string[]
    return colors.length > 0 ? colors : DEFAULT_COLORS
  } catch {
    return DEFAULT_COLORS
  }
}

function loadNewlyUnlocked(): string[] {
  try {
    return JSON.parse(localStorage.getItem(NEW_KEY) || '[]')
  } catch {
    return []
  }
}

function saveNewlyUnlocked(ids: string[]) {
  localStorage.setItem(NEW_KEY, JSON.stringify(ids))
}

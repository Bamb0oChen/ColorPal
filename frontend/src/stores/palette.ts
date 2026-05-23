import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { UploadResponse } from '@/api/photo'
import { findClosestColor, getColorById, type ColorItem } from '@/utils/constants'

const STORAGE_KEY = 'colorpal.palette'
const LAST_ANALYSIS_KEY = 'colorpal.last-analysis'
const COLLECTION_NOTICE_KEY = 'colorpal.collection-notice'
const DEFAULT_COLORS = ['#ff6b6b', '#4ecdc4', '#ffe66d']

export const usePaletteStore = defineStore('palette', () => {
  const collectedColors = ref<string[]>(loadColors())
  const lastAnalysis = ref<UploadResponse | null>(loadLastAnalysis())
  const unseenCollectionIds = ref<string[]>(loadNoticeIds())

  const accentColor = computed(() => collectedColors.value[0] || DEFAULT_COLORS[0])
  const hasCollectionNotice = computed(() => unseenCollectionIds.value.length > 0)
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

  const addColorFromImageName = (fileName: string) => {
    const next = colorFromText(fileName)
    collectedColors.value = [next, ...collectedColors.value].slice(0, 8)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectedColors.value))
  }

  const addAnalysisResult = (result: UploadResponse) => {
    const previousIds = new Set(collectedColorItems.value.map((color) => color.id))
    const matchedColors = [
      result.analysis.dominant_color,
      ...result.analysis.palette,
    ]
      .map(normalizeHex)
      .filter((color): color is string => Boolean(color))
      .map((color) => findClosestColor(color))
      .filter((color): color is ColorItem => Boolean(color))

    const newIds = matchedColors
      .filter((color) => !previousIds.has(color.id))
      .map((color) => color.id)
    if (newIds.length) {
      unseenCollectionIds.value = [...new Set([...unseenCollectionIds.value, ...newIds])]
      localStorage.setItem(COLLECTION_NOTICE_KEY, JSON.stringify(unseenCollectionIds.value))
    }

    const nextColors = [
      ...matchedColors.map((color) => color.hex),
      ...collectedColors.value.map(normalizeHex),
    ]
      .filter((color): color is string => Boolean(color))

    collectedColors.value = [...new Set(nextColors)].slice(0, 8)
    lastAnalysis.value = {
      ...result,
      analysis: {
        ...result.analysis,
        dominant_color: matchedColors[0]?.hex ?? DEFAULT_COLORS[0],
        palette: matchedColors.map((color) => color.hex),
      },
    }

    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectedColors.value))
    localStorage.setItem(LAST_ANALYSIS_KEY, JSON.stringify(lastAnalysis.value))
  }

  /** 按色值命中解锁（Homepage AI 返回 hex 时用） */
  function addColor(hex: string) {
    const match = findClosestColor(hex)
    const colorHex = match?.hex || hex
    collectedColors.value = [colorHex, ...collectedColors.value.filter((c) => c !== colorHex)].slice(0, 8)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectedColors.value))

    if (match && !collectedColorItems.value.some((c) => c.id === match.id)) {
      if (!unseenCollectionIds.value.includes(match.id)) {
        unseenCollectionIds.value.push(match.id)
        localStorage.setItem(COLLECTION_NOTICE_KEY, JSON.stringify(unseenCollectionIds.value))
      }
    }
  }

  /** 按色码 ID 直接解锁 */
  function unlockColorById(colorId: string) {
    if (collectedColorItems.value.some((c) => c.id === colorId)) return
    const match = getColorById(colorId)
    if (!match) return

    collectedColors.value = [match.hex, ...collectedColors.value.filter((c) => c !== match.hex)].slice(0, 8)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectedColors.value))

    if (!unseenCollectionIds.value.includes(match.id)) {
      unseenCollectionIds.value.push(match.id)
      localStorage.setItem(COLLECTION_NOTICE_KEY, JSON.stringify(unseenCollectionIds.value))
    }
  }

  const clearCollectionNotice = () => {
    unseenCollectionIds.value = []
    localStorage.removeItem(COLLECTION_NOTICE_KEY)
  }

  return {
    collectedColors,
    collectedColorItems,
    accentColor,
    lastAnalysis,
    hasCollectionNotice,
    unseenCollectionIds,
    addColorFromImageName,
    addColor,
    unlockColorById,
    addAnalysisResult,
    clearCollectionNotice,
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

function loadLastAnalysis(): UploadResponse | null {
  const raw = localStorage.getItem(LAST_ANALYSIS_KEY)
  if (!raw) return null

  try {
    return JSON.parse(raw) as UploadResponse
  } catch {
    return null
  }
}

function loadNoticeIds(): string[] {
  const raw = localStorage.getItem(COLLECTION_NOTICE_KEY)
  if (!raw) return []

  try {
    const ids = JSON.parse(raw) as string[]
    return Array.isArray(ids) ? ids.filter((id) => typeof id === 'string') : []
  } catch {
    return []
  }
}

function normalizeHex(color: string): string | null {
  if (!/^#[0-9a-fA-F]{6}$/.test(color)) return null
  return color.toUpperCase()
}

function colorFromText(text: string): string {
  let hash = 0
  for (const char of text) hash = (hash * 31 + char.charCodeAt(0)) >>> 0
  const hue = hash % 360
  return hslToHex(hue, 74, 58)
}

function hslToHex(h: number, s: number, l: number): string {
  const light = l / 100
  const saturation = s / 100
  const chroma = (1 - Math.abs(2 * light - 1)) * saturation
  const x = chroma * (1 - Math.abs(((h / 60) % 2) - 1))
  const m = light - chroma / 2
  const [r, g, b] =
    h < 60
      ? [chroma, x, 0]
      : h < 120
        ? [x, chroma, 0]
        : h < 180
          ? [0, chroma, x]
          : h < 240
            ? [0, x, chroma]
            : h < 300
              ? [x, 0, chroma]
              : [chroma, 0, x]

  return `#${[r, g, b]
    .map((value) =>
      Math.round((value + m) * 255)
        .toString(16)
        .padStart(2, '0'),
    )
    .join('')}`
}

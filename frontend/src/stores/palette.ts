import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const STORAGE_KEY = 'colorpal.palette'
const DEFAULT_COLORS = ['#ff6b6b', '#4ecdc4', '#ffe66d']

export const usePaletteStore = defineStore('palette', () => {
  const collectedColors = ref<string[]>(loadColors())

  const accentColor = computed(() => collectedColors.value[0] || DEFAULT_COLORS[0])

  const addColorFromImageName = (fileName: string) => {
    const next = colorFromText(fileName)
    collectedColors.value = [next, ...collectedColors.value].slice(0, 8)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectedColors.value))
  }

  return { collectedColors, accentColor, addColorFromImageName }
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

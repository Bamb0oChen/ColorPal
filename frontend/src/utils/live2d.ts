export const defaultPetModel = '/vendor/live2d/wanko/wanko.model.json'

export const cubism2RuntimeScript = '/vendor/live2d/runtime/live2d.min.js'

export type PetDisplaySize = 'compact' | 'hero' | 'panel' | 'avatar'

export type PetDisplayEvent = 'idle' | 'tap' | 'feeding' | 'success' | 'evolve'

const MODEL_VARIANTS: { name: string; match: (h: number, s: number, l: number) => boolean }[] = [
  { name: 'red', match: (h) => h < 20 || h >= 340 },
  { name: 'darkred', match: (h, s, l) => (h < 20 || h >= 340) && l < 0.35 },
  { name: 'orange', match: (h) => h >= 20 && h < 50 },
  { name: 'yellow', match: (h) => h >= 50 && h < 75 },
  { name: 'green', match: (h) => h >= 75 && h < 160 },
  { name: 'blue', match: (h) => h >= 160 && h < 260 },
  { name: 'purple', match: (h) => h >= 260 && h < 340 },
  { name: 'black', match: (_h, _s, l) => l < 0.2 },
  { name: 'white', match: (_h, _s, l) => l > 0.9 },
  { name: 'grey', match: (_h, s) => s < 0.1 },
]

export function makeModelSettings(color: string): string {
  const hex = color.replace('#', '')
  const r = parseInt(hex.slice(0, 2), 16) / 255
  const g = parseInt(hex.slice(2, 4), 16) / 255
  const b = parseInt(hex.slice(4, 6), 16) / 255

  const max = Math.max(r, g, b), min = Math.min(r, g, b)
  const l = (max + min) / 2
  if (max === min) return defaultPetModel
  const d = max - min
  const s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
  let h = 0
  if (max === r) h = (g - b) / d + (g < b ? 6 : 0)
  else if (max === g) h = (b - r) / d + 2
  else h = (r - g) / d + 4
  h *= 60

  for (const variant of MODEL_VARIANTS) {
    if (variant.match(h, s, l)) {
      return `/vendor/live2d/wanko/wanko_${variant.name}.model.json`
    }
  }
  return defaultPetModel
}

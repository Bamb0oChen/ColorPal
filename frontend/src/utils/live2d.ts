import { findClosestColor } from '@/utils/constants'

export const defaultPetModel = '/vendor/live2d/wanko/wanko.model.json'

export const cubism2RuntimeScript = '/vendor/live2d/runtime/live2d.min.js'

export type PetDisplaySize = 'compact' | 'hero' | 'panel' | 'avatar'

export type PetDisplayEvent = 'idle' | 'tap' | 'feeding' | 'success' | 'evolve'

// ---------------------------------------------------------------------------
// Texture color matching — dictionary from album color ID → texture filename
// ---------------------------------------------------------------------------

const MODEL_DIR = '/vendor/live2d/wanko'

const COLOR_TO_TEXTURE: Record<string, string> = {
  // 红色系
  'red_red':       'texture_07_topred.png',
  'red_vermilion': 'texture_07_topred.png',
  'red_rose':      'texture_07_topred.png',
  'red_burgundy':  'texture_02_finered.png',
  'red_brick':     'texture_02_finered.png',
  'red_pink':      'texture_00_white.png',

  // 橙色系
  'orange_orange':    'texture_03_orange.png',
  'orange_tangerine': 'texture_03_orange.png',
  'orange_apricot':   'texture_00_white.png',
  'orange_amber':     'texture_03_orange.png',

  // 黄色系
  'yellow_bright':  'texture_06_yellow.png',
  'yellow_gold':    'texture_06_yellow.png',
  'yellow_lemon':   'texture_06_yellow.png',
  'yellow_mustard': 'texture_06_yellow.png',
  'yellow_cream':   'texture_00_white.png',

  // 绿色系
  'green_grass':   'texture_04_green.png',
  'green_emerald': 'texture_04_green.png',
  'green_olive':   'texture_04_green.png',
  'green_mint':    'texture_04_green.png',
  'green_dark':    'texture_04_green.png',
  'green_teal':    'texture_04_green.png',

  // 蓝色系
  'blue_sky':    'texture_01_blue.png',
  'blue_lake':   'texture_01_blue.png',
  'blue_navy':   'texture_01_blue.png',
  'blue_indigo': 'texture_05_purple.png',
  'blue_cobalt': 'texture_01_blue.png',
  'blue_ice':    'texture_00_white.png',

  // 紫色系
  'purple_violet':   'texture_05_purple.png',
  'purple_lavender': 'texture_05_purple.png',
  'purple_magenta':  'texture_05_purple.png',
  'purple_grape':    'texture_05_purple.png',
  'purple_lilac':    'texture_05_purple.png',

  // 无彩色
  'gray_black':  'texture_09_black.png',
  'gray_white':  'texture_00_white.png',
  'gray_silver': 'texture_08_grey.png',
  'gray_gold':   'texture_06_yellow.png',
}

/** Return the texture filename for a hex color, or default white. */
export function getTextureForColor(hex: string): string {
  const closest = findClosestColor(hex)
  return closest ? (COLOR_TO_TEXTURE[closest.id] ?? 'texture_00_white.png') : 'texture_00_white.png'
}

/**
 * Fetch the base model.json and replace textures with the color-matched file.
 * Returns the modified settings object with absolute paths for reliable loading.
 */
export async function makeModelSettings(hex: string): Promise<Record<string, unknown>> {
  const baseUrl = window.location.origin + MODEL_DIR
  const modelJsonUrl = `${baseUrl}/wanko.model.json`
  const res = await fetch(modelJsonUrl)
  const settings: Record<string, unknown> = await res.json()

  const textureFile = getTextureForColor(hex)

  settings.url = modelJsonUrl
  settings.model = `${baseUrl}/wanko.moc`
  settings.textures = [`${baseUrl}/wanko.1024/${textureFile}`]

  const motions = settings.motions as Record<string, { file: string; fade_in: number; fade_out: number }[]>
  for (const key of Object.keys(motions)) {
    motions[key] = motions[key].map((m) => ({
      ...m,
      file: `${baseUrl}/motions/${m.file.split('/').pop()}`,
    }))
  }

  return settings
}

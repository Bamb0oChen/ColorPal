<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import PetDisplay from '@/components/PetDisplay.vue'
import { uploadAndAnalyze } from '@/api/photo'
import { usePaletteStore } from '@/stores/palette'
import { usePetStore } from '@/stores/pet'
import { useSessionStore } from '@/stores/session'
import { createDemoPet } from '@/utils/demoPet'
import {
  findClosestColor,
} from '@/utils/constants'

const paletteStore = usePaletteStore()
const petStore = usePetStore()
const sessionStore = useSessionStore()
const isDevMode = import.meta.env.DEV
const isTestingColor = ref(false)
const testColorIndex = ref(0)

const TEST_COLORS = [
  { name: '钴蓝', hex: '#0047AB' },
  { name: '朱红', hex: '#E34234' },
  { name: '紫罗兰', hex: '#8F00FF' },
  { name: '翠绿', hex: '#50C878' },
]

const nextTestColor = computed(() => {
  const startIndex = testColorIndex.value % TEST_COLORS.length
  const collectedIds = new Set(paletteStore.collectedColorItems.map((color) => color.id))
  const orderedColors = [
    ...TEST_COLORS.slice(startIndex),
    ...TEST_COLORS.slice(0, startIndex),
  ]

  return orderedColors.find((color) => {
    const matched = findClosestColor(color.hex)
    return matched && !collectedIds.has(matched.id)
  }) ?? TEST_COLORS[startIndex]
})
const displayPet = computed(() => petStore.petInfo ?? createDemoPet(paletteStore.accentColor))
const analysisResult = computed(() => paletteStore.lastAnalysis)
const hasAnalysisResult = computed(() => Boolean(analysisResult.value))
const palette = computed(() => {
  if (!analysisResult.value) return []

  const colors = [
      analysisResult.value.analysis.dominant_color,
      ...analysisResult.value.analysis.palette,
    ]
    .map(toReferenceHex)
    .filter((color): color is string => Boolean(color))

  return colors.slice(0, 5)
})
const paletteSwatches = computed(() =>
  palette.value.map((color) => ({
    color,
    textColor: readableTextColor(color),
    textShadow: readableTextColor(color) === '#ffffff'
      ? '0 1px 4px rgba(0, 0, 0, 0.36)'
      : '0 1px 0 rgba(255, 255, 255, 0.48)',
  })),
)
const dominantColor = computed(() => palette.value[0] || paletteStore.accentColor)
const matchedColor = computed(() => findClosestColor(dominantColor.value))
const colorName = computed(() => matchedColor.value?.name ?? '颜色')
const referenceColor = computed(() => matchedColor.value?.hex ?? dominantColor.value)
const needsAccentSupport = computed(() => isNearWhiteColor(referenceColor.value))
const score = computed(() =>
  analysisResult.value?.analysis.score ?? 0,
)
const comment = computed(() =>
  analysisResult.value?.analysis.comment || '先采一张照片，小彩会把真实分析结果放在这里。',
)
const energyGain = computed(() =>
  analysisResult.value?.energy_change.total ?? 0,
)

onMounted(async () => {
  if (!sessionStore.isLoggedIn || petStore.petInfo) return

  try {
    await petStore.fetchProfile()
  } catch (err) {
    console.warn('[ResultView] Profile fetch failed, using demo pet.', err)
  }
})

const handleDevColorTest = async () => {
  if (isTestingColor.value) return

  isTestingColor.value = true
  const sample = nextTestColor.value

  try {
    const file = await createSolidColorFile(sample.hex, sample.name)
    const result = await uploadAndAnalyze(file)
    paletteStore.addAnalysisResult(result)
    petStore.updateEnergy(result.energy_change)
    if (sessionStore.isLoggedIn) {
      await petStore.fetchProfile().catch((err) => {
        console.warn('[ResultView] Profile refresh failed after color test.', err)
      })
    }
    testColorIndex.value += 1
  } catch (err) {
    console.error('[ResultView] Dev color test failed.', err)
  } finally {
    isTestingColor.value = false
  }
}

function toReferenceHex(color: string): string | null {
  return findClosestColor(color)?.hex ?? null
}

function createSolidColorFile(hex: string, name: string): Promise<File> {
  return new Promise((resolve, reject) => {
    const canvas = document.createElement('canvas')
    canvas.width = 640
    canvas.height = 420

    const context = canvas.getContext('2d')
    if (!context) {
      reject(new Error('Canvas unavailable'))
      return
    }

    context.fillStyle = hex
    context.fillRect(0, 0, canvas.width, canvas.height)
    context.fillStyle = 'rgba(255, 255, 255, 0.22)'
    context.beginPath()
    context.arc(190, 260, 120, 0, Math.PI * 2)
    context.fill()

    canvas.toBlob((blob) => {
      if (!blob) {
        reject(new Error('Canvas export failed'))
        return
      }
      resolve(new File([blob], `colorpal-${name}.png`, { type: 'image/png' }))
    }, 'image/png')
  })
}

function readableTextColor(hex: string): '#20242e' | '#ffffff' {
  const rgb = parseHexColor(hex)
  if (!rgb) return '#20242e'
  const luminance = (0.2126 * rgb.r + 0.7152 * rgb.g + 0.0722 * rgb.b) / 255
  return luminance > 0.68 ? '#20242e' : '#ffffff'
}

function isNearWhiteColor(hex: string): boolean {
  const rgb = parseHexColor(hex)
  if (!rgb) return false

  const max = Math.max(rgb.r, rgb.g, rgb.b)
  const min = Math.min(rgb.r, rgb.g, rgb.b)
  const lightness = (max + min) / 510

  return lightness >= 0.82
}

function parseHexColor(hex: string): { r: number; g: number; b: number } | null {
  if (!/^#[0-9a-fA-F]{6}$/.test(hex)) return null
  const value = hex.replace('#', '')

  return {
    r: parseInt(value.slice(0, 2), 16),
    g: parseInt(value.slice(2, 4), 16),
    b: parseInt(value.slice(4, 6), 16),
  }
}
</script>

<template>
  <main class="result-page" :style="{ '--accent-color': referenceColor }">
    <nav class="page-nav">
      <RouterLink to="/">继续采色</RouterLink>
      <RouterLink
        class="collection-nav-link"
        :class="{ 'has-notice': paletteStore.hasCollectionNotice }"
        to="/collection"
      >
        图鉴
      </RouterLink>
      <RouterLink to="/profile">小彩状态</RouterLink>
      <button
        v-if="isDevMode"
        class="dev-color-button"
        type="button"
        :disabled="isTestingColor"
        @click="handleDevColorTest"
      >
        {{ isTestingColor ? '换色中...' : `换测试色：${nextTestColor.name}` }}
      </button>
    </nav>

    <section class="result-layout">
      <div class="result-panel">
        <PetDisplay
          class="result-pet"
          :pet="displayPet"
          size="avatar"
          event="success"
          :show-stats="false"
        />
        <p class="section-label">本次投喂</p>
        <h1 v-if="hasAnalysisResult">
          小彩吃到了 “<span
            class="color-acrylic color-name"
            :class="{ 'needs-support': needsAccentSupport }"
          >{{ colorName }}</span>”
        </h1>
        <h1 v-else>还没有本次分析</h1>
        <p class="comment">{{ comment }}</p>

        <div class="score-row">
          <span>色彩评分</span>
          <strong
            class="color-acrylic"
            :class="{ 'needs-support': needsAccentSupport }"
          >
            {{ score }}
          </strong>
        </div>

        <div v-if="palette.length" class="palette-row" aria-label="本次颜色">
          <span
            v-for="(swatch, index) in paletteSwatches"
            :key="`${swatch.color}-${index}`"
            class="swatch"
            :style="{ backgroundColor: swatch.color }"
          >
            <span
              class="swatch-label"
              :style="{ color: swatch.textColor, textShadow: swatch.textShadow }"
            >
              {{ swatch.color }}
            </span>
          </span>
        </div>

        <div class="energy-card">
          <span>能量增加</span>
          <strong
            class="color-acrylic energy-gain"
            :class="{ 'needs-support': needsAccentSupport }"
          >
            +{{ energyGain }}
          </strong>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.result-page {
  min-height: 100vh;
  padding: 28px;
  background:
    radial-gradient(circle at 16% 18%, color-mix(in srgb, var(--accent-color), transparent 72%), transparent 24%),
    linear-gradient(180deg, #ffffff, color-mix(in srgb, var(--accent-color), white 90%));
  color: #252525;
}

.page-nav {
  width: min(1060px, 100%);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin: 0 auto 18px;
}

.page-nav a,
.dev-color-button {
  position: relative;
  min-height: 38px;
  display: inline-grid;
  place-items: center;
  padding: 0 14px;
  border: 1px solid rgba(30, 30, 30, 0.09);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.74);
  color: #333;
  font-size: 14px;
  font-weight: 750;
  text-decoration: none;
}

.collection-nav-link.has-notice::after {
  content: '';
  position: absolute;
  top: 5px;
  right: 7px;
  width: 8px;
  height: 8px;
  border: 2px solid #fff;
  border-radius: 50%;
  background: #ff3b30;
  box-shadow: 0 4px 12px rgba(255, 59, 48, 0.36);
}

.dev-color-button {
  cursor: pointer;
}

.dev-color-button:disabled {
  cursor: wait;
  opacity: 0.68;
}

.result-layout {
  width: min(1060px, 100%);
  min-height: calc(100vh - 102px);
  display: grid;
  place-items: center;
  margin: 0 auto;
}

.result-panel {
  position: relative;
  width: min(620px, 100%);
  display: grid;
  gap: 20px;
  padding: 164px 28px 28px;
  border: 1px solid rgba(31, 31, 31, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 18px 52px rgba(42, 42, 42, 0.08);
  backdrop-filter: blur(18px);
}

.result-pet {
  position: absolute;
  top: 18px;
  left: 50%;
  transform: translateX(-50%);
}

.section-label,
.comment {
  margin: 0;
}

.section-label {
  color: var(--accent-color);
  font-size: 13px;
  font-weight: 850;
}

h1 {
  max-width: 520px;
  margin: 0;
  font-size: clamp(32px, 5vw, 58px);
  line-height: 1.02;
  letter-spacing: 0;
}

.comment {
  color: #69645e;
  font-size: 16px;
  line-height: 1.7;
}

.score-row,
.energy-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.score-row {
  padding-top: 8px;
}

.score-row span,
.energy-card span {
  color: #6d6762;
  font-weight: 750;
}

.score-row strong {
  color: var(--accent-color);
  font-size: 64px;
  line-height: 0.9;
}

.color-acrylic {
  --spot-width: calc((100% + 42px) * 0.6);
  --spot-height: calc((100% + 30px) * 0.6);
  --spot-x: 38%;
  --spot-y: 64%;
  position: relative;
  isolation: isolate;
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 0 4px;
  color: var(--accent-color);
}

.color-acrylic.needs-support {
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.72),
    0 2px 10px rgba(31, 36, 50, 0.32),
    0 0 1px rgba(31, 36, 50, 0.52);
}

.color-acrylic.needs-support::before {
  content: '';
  position: absolute;
  z-index: -1;
  left: var(--spot-x);
  top: var(--spot-y);
  width: var(--spot-width);
  height: var(--spot-height);
  border-radius: 50%;
  background:
    radial-gradient(
      ellipse at center,
      color-mix(in srgb, var(--accent-color), transparent 34%) 0 18%,
      color-mix(in srgb, var(--accent-color), transparent 58%) 42%,
      color-mix(in srgb, var(--accent-color), transparent 80%) 68%,
      transparent 100%
    );
  filter: blur(8px);
  transform: translate(-50%, -50%);
}

.color-name {
  --spot-width: calc((100% + 54px) * 0.6);
  --spot-height: calc((100% + 32px) * 0.6);
  transform: translateY(-0.04em);
}

.palette-row {
  display: grid;
  grid-template-columns: repeat(5, minmax(34px, 1fr));
  gap: 10px;
}

.swatch {
  display: grid;
  place-items: center;
  min-height: 54px;
  min-width: 0;
  border-radius: 8px;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);
}

.swatch-label {
  max-width: calc(100% - 8px);
  padding: 4px 6px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 11px;
  font-weight: 800;
  line-height: 1;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.energy-card {
  min-height: 64px;
  padding: 0 18px;
  border-radius: 8px;
  background: color-mix(in srgb, var(--accent-color), white 86%);
}

.energy-card strong {
  color: var(--accent-color);
  font-size: 32px;
}

.energy-gain {
  --spot-width: calc((100% + 34px) * 0.6);
  --spot-height: calc((100% + 24px) * 0.6);
  padding: 0 4px;
}

@media (max-width: 760px) {
  .result-page {
    padding: 18px;
  }

  .page-nav {
    justify-content: center;
  }

  .result-layout {
    min-height: auto;
  }

  .result-panel {
    padding: 154px 22px 22px;
  }

  .result-pet {
    top: 16px;
  }

  h1 {
    font-size: 34px;
  }
}
</style>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import DesktopDropZone from '@/components/DesktopDropZone.vue'
import LoginPanel from '@/components/LoginPanel.vue'
import MobileCaptureButton from '@/components/MobileCaptureButton.vue'
import PetDisplay from '@/components/PetDisplay.vue'
import { useDeviceMode } from '@/composables/useDeviceMode'
import { uploadAndAnalyze } from '@/api/photo'
import { ALL_COLORS, ColorFamilyLabel, RarityLabel } from '@/utils/constants'
import { usePaletteStore } from '@/stores/palette'
import { usePetStore } from '@/stores/pet'
import { useSessionStore } from '@/stores/session'
import { createDemoPet } from '@/utils/demoPet'
import type { PetDisplayEvent } from '@/utils/live2d'

const sessionStore = useSessionStore()
const paletteStore = usePaletteStore()
const petStore = usePetStore()
const router = useRouter()
const { isMobile } = useDeviceMode()
const petEvent = ref<PetDisplayEvent>('idle')
const isAnalyzing = ref(false)
const analysisError = ref('')

const pageStyle = computed(() => ({
  '--accent-color': paletteStore.accentColor,
}))

const displayPet = computed(() => petStore.petInfo ?? createDemoPet(paletteStore.accentColor))
const collectedItems = computed(() => paletteStore.collectedColorItems)
const collectedCount = computed(() => collectedItems.value.length)
const recentColorItems = computed(() => collectedItems.value.slice(0, 5))
const latestColorItem = computed(() => collectedItems.value[0])
const colorSummary = computed(() => {
  if (!recentColorItems.value.length) {
    return `当前已识别 0 / ${ALL_COLORS.length} 种图鉴标准颜色，先采一张照片开始收集。`
  }

  const recentNames = recentColorItems.value.map((color) => color.name).join('、')
  return `当前已识别 ${collectedCount.value} / ${ALL_COLORS.length} 种图鉴标准颜色，最近收集：${recentNames}。`
})
const latestColorDescription = computed(() => {
  if (!latestColorItem.value) return '等待第一张照片'

  const color = latestColorItem.value
  return `${color.name} · ${ColorFamilyLabel[color.family]} · ${RarityLabel[color.rarity]}`
})
const progressPercent = computed(() =>
  Math.round((collectedCount.value / ALL_COLORS.length) * 100),
)

watch(
  () => sessionStore.isLoggedIn,
  async (isLoggedIn) => {
    if (!isLoggedIn || petStore.petInfo) return
    try {
      await petStore.fetchProfile()
    } catch (err) {
      console.warn('[HomeView] Profile fetch failed, using demo pet.', err)
    }
  },
  { immediate: true },
)

const handleImageSelected = async (file: File) => {
  if (isAnalyzing.value) return

  isAnalyzing.value = true
  analysisError.value = ''
  petEvent.value = 'feeding'

  try {
    const result = await uploadAndAnalyze(file)
    paletteStore.addAnalysisResult(result)
    petStore.updateEnergy(result.energy_change)
    if (sessionStore.isLoggedIn) {
      await petStore.fetchProfile().catch((err) => {
        console.warn('[HomeView] Profile refresh failed after analysis.', err)
      })
    }
    await wait(520)
    petEvent.value = 'success'
    await wait(280)
    await router.push({ name: 'result' })
  } catch (err) {
    console.error('[HomeView] Photo analysis failed.', err)
    analysisError.value = '照片分析暂时失败，请稍后再试一次。'
    petEvent.value = 'idle'
  } finally {
    isAnalyzing.value = false
  }
}

function wait(ms: number) {
  return new Promise<void>((resolve) => {
    window.setTimeout(resolve, ms)
  })
}
</script>

<template>
  <section class="home-page" :style="pageStyle">
    <div class="wash wash-one" />
    <div class="wash wash-two" />

    <div v-if="!sessionStore.isLoggedIn" class="login-layout">
      <LoginPanel />
      <PetDisplay :pet="displayPet" size="panel" :interactive="false" />
    </div>

    <div v-else class="main-layout">
      <section class="hero-panel">
        <div class="hero-copy">
          <p class="eyebrow">ColorPal</p>
          <h1>把现实里的颜色收进你的图鉴</h1>
          <p class="summary">{{ colorSummary }}</p>
          <div class="progress-track" aria-label="收集进度">
            <span :style="{ width: progressPercent + '%' }" />
          </div>
          <p class="latest-color">{{ latestColorDescription }}</p>
        </div>

        <div class="spirit-stage">
          <PetDisplay :pet="displayPet" :event="petEvent" />
        </div>
      </section>

      <section class="capture-panel">
        <div class="palette-strip" aria-label="已收集颜色">
          <span
            v-for="color in recentColorItems"
            :key="color.id"
            class="color-chip"
            :title="`${color.name} · ${color.english}`"
            :aria-label="`${color.name}，${ColorFamilyLabel[color.family]}，${RarityLabel[color.rarity]}`"
          >
            <span class="swatch" :style="{ backgroundColor: color.hex }" />
            <span>{{ color.name }}</span>
          </span>
        </div>

        <p v-if="isAnalyzing" class="analysis-status">正在分析照片颜色...</p>
        <p v-if="analysisError" class="analysis-error">{{ analysisError }}</p>

        <DesktopDropZone v-if="!isMobile" @image-selected="handleImageSelected" />
        <div v-else class="mobile-action">
          <MobileCaptureButton @image-selected="handleImageSelected" />
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.home-page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(255, 255, 255, 0.98)),
    color-mix(in srgb, var(--accent-color), white 88%);
  color: #202020;
}

.wash {
  position: fixed;
  pointer-events: none;
  border-radius: 999px;
  background: color-mix(in srgb, var(--accent-color), transparent 76%);
  filter: blur(52px);
}

.wash-one {
  top: -90px;
  right: -80px;
  width: 280px;
  height: 280px;
}

.wash-two {
  left: -120px;
  bottom: -130px;
  width: 320px;
  height: 320px;
  opacity: 0.42;
}

.login-layout,
.main-layout {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}

.login-layout {
  display: grid;
  grid-template-columns: minmax(300px, 420px) minmax(220px, 1fr);
  align-items: center;
  gap: 72px;
  width: min(1080px, calc(100vw - 48px));
  margin: 0 auto;
}

.main-layout {
  display: grid;
  grid-template-columns: minmax(320px, 0.9fr) minmax(360px, 1.1fr);
  align-items: center;
  gap: 34px;
  width: min(1080px, calc(100vw - 48px));
  margin: 0 auto;
  padding: 108px 0 56px;
}

.hero-panel,
.capture-panel {
  display: grid;
  gap: 24px;
}

.hero-panel {
  align-content: center;
}

.eyebrow,
.summary,
.latest-color,
h1 {
  margin: 0;
}

.eyebrow {
  color: var(--accent-color);
  font-size: 13px;
  font-weight: 850;
  text-transform: uppercase;
}

h1 {
  margin-top: 12px;
  max-width: 9em;
  font-size: clamp(42px, 5vw, 68px);
  line-height: 0.98;
  letter-spacing: 0;
}

.summary {
  margin-top: 18px;
  max-width: 460px;
  color: #606060;
  line-height: 1.7;
}

.latest-color {
  margin-top: 12px;
  color: var(--accent-color);
  font-size: 14px;
  font-weight: 850;
}

.progress-track {
  width: min(360px, 100%);
  height: 10px;
  margin-top: 26px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(20, 20, 20, 0.08);
}

.progress-track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--accent-color);
}

.spirit-stage {
  display: grid;
  justify-items: start;
}

.capture-panel {
  justify-items: center;
}

.analysis-status,
.analysis-error {
  margin: 0;
  color: #5f6470;
  font-size: 14px;
  font-weight: 700;
}

.analysis-error {
  color: #c24150;
}

.palette-strip {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  max-width: 420px;
  padding: 8px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
}

.color-chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 34px;
  padding: 0 10px 0 7px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 7px;
  background: rgba(255, 255, 255, 0.82);
  color: #343434;
  font-size: 13px;
  font-weight: 800;
  white-space: nowrap;
}

.swatch {
  width: 22px;
  height: 22px;
  flex: 0 0 auto;
  border-radius: 6px;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);
}

.mobile-action {
  display: grid;
  place-items: center;
  min-height: 126px;
}

@media (max-width: 760px) {
  .home-page {
    padding-bottom: 84px;
  }

  .login-layout {
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 28px 0;
  }

  .login-layout :deep(.pet-display) {
    order: -1;
    justify-self: center;
  }

  .main-layout {
    grid-template-columns: 1fr;
    gap: 24px;
    width: min(420px, calc(100vw - 32px));
    padding: 30px 0 36px;
  }

  h1 {
    max-width: 10em;
    font-size: 38px;
  }

  .spirit-stage,
  .capture-panel {
    justify-items: center;
  }

  .hero-copy {
    text-align: center;
  }
}
</style>

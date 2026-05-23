<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import DesktopDropZone from '@/components/DesktopDropZone.vue'
import LoginPanel from '@/components/LoginPanel.vue'
import MobileCaptureButton from '@/components/MobileCaptureButton.vue'
import PetDisplay from '@/components/PetDisplay.vue'
import { useDeviceMode } from '@/composables/useDeviceMode'
import { ALL_COLORS } from '@/utils/constants'
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

const pageStyle = computed(() => ({
  '--accent-color': paletteStore.accentColor,
}))

const displayPet = computed(() => petStore.petInfo ?? createDemoPet(paletteStore.accentColor))
const collectedCount = computed(() => paletteStore.collectedColors.length)
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
  paletteStore.addColorFromImageName(file.name)
  petStore.updateEnergy({ r: 8, g: 6, b: 4, total: 12 })
  petEvent.value = 'feeding'
  await wait(520)
  petEvent.value = 'success'
  await wait(280)
  await router.push({ name: 'result' })
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
          <p class="summary">
            当前已识别 {{ collectedCount }} / {{ ALL_COLORS.length }} 种标准颜色，页面主题会跟随最近收集的颜色变化。
          </p>
          <div class="progress-track" aria-label="收集进度">
            <span :style="{ width: progressPercent + '%' }" />
          </div>
        </div>

        <div class="spirit-stage">
          <PetDisplay :pet="displayPet" :event="petEvent" />
        </div>
      </section>

      <section class="capture-panel">
        <div class="palette-strip" aria-label="已收集颜色">
          <span
            v-for="color in paletteStore.collectedColors"
            :key="color"
            class="swatch"
            :style="{ backgroundColor: color }"
          />
        </div>

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

.palette-strip {
  display: inline-flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  max-width: 420px;
  padding: 8px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.72);
}

.swatch {
  width: 22px;
  height: 22px;
  border-radius: 50%;
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

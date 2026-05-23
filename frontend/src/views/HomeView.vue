<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import DesktopDropZone from '@/components/DesktopDropZone.vue'
import LoginPanel from '@/components/LoginPanel.vue'
import MobileCaptureButton from '@/components/MobileCaptureButton.vue'
import PetDisplay from '@/components/PetDisplay.vue'
import { useDeviceMode } from '@/composables/useDeviceMode'
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
  <main class="home-page" :style="pageStyle">
    <div class="wash wash-one" />
    <div class="wash wash-two" />

    <section v-if="!sessionStore.isLoggedIn" class="login-layout">
      <LoginPanel />
      <PetDisplay :pet="displayPet" size="panel" :interactive="false" />
    </section>

    <section v-else class="main-layout">
      <header class="topbar">
        <div>
          <p class="brand">ColorPal</p>
          <p class="welcome">Hi, {{ sessionStore.session?.display_name }}</p>
        </div>
        <button type="button" class="ghost-button" @click="sessionStore.logout">退出</button>
      </header>

      <div class="stage">
        <div class="palette-strip" aria-label="已收集颜色">
          <span
            v-for="color in paletteStore.collectedColors"
            :key="color"
            class="swatch"
            :style="{ backgroundColor: color }"
          />
        </div>

        <PetDisplay :pet="displayPet" :event="petEvent" />

        <DesktopDropZone v-if="!isMobile" @image-selected="handleImageSelected" />
        <div v-else class="mobile-action">
          <MobileCaptureButton @image-selected="handleImageSelected" />
        </div>
      </div>
    </section>
  </main>
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
  grid-template-rows: auto 1fr;
  padding: 26px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.brand,
.welcome {
  margin: 0;
}

.brand {
  color: var(--accent-color);
  font-size: 14px;
  font-weight: 800;
}

.welcome {
  margin-top: 4px;
  color: #555;
}

.ghost-button {
  min-width: 72px;
  height: 38px;
  border: 1px solid rgba(30, 30, 30, 0.12);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.68);
  color: #333;
  cursor: pointer;
}

.stage {
  min-height: calc(100vh - 120px);
  display: grid;
  place-items: center;
  align-content: center;
  gap: 24px;
}

.palette-strip {
  display: inline-flex;
  gap: 8px;
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
    padding: 18px;
  }

  .stage {
    min-height: calc(100vh - 104px);
    gap: 18px;
  }
}
</style>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import PetDisplay from '@/components/PetDisplay.vue'
import { usePaletteStore } from '@/stores/palette'
import { usePetStore } from '@/stores/pet'
import { useSessionStore } from '@/stores/session'
import { createDemoPet } from '@/utils/demoPet'

const paletteStore = usePaletteStore()
const petStore = usePetStore()
const sessionStore = useSessionStore()

const displayPet = computed(() => petStore.petInfo ?? createDemoPet(paletteStore.accentColor))
const palette = computed(() => paletteStore.collectedColors.slice(0, 5))
const score = computed(() => Math.min(96, 70 + palette.value.length * 4))
const energyGain = computed(() => Math.max(12, palette.value.length * 6))

onMounted(async () => {
  if (!sessionStore.isLoggedIn || petStore.petInfo) return

  try {
    await petStore.fetchProfile()
  } catch (err) {
    console.warn('[ResultView] Profile fetch failed, using demo pet.', err)
  }
})
</script>

<template>
  <main class="result-page" :style="{ '--accent-color': paletteStore.accentColor }">
    <nav class="page-nav">
      <RouterLink to="/">继续采色</RouterLink>
      <RouterLink to="/profile">小彩状态</RouterLink>
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
        <h1>小彩吃到了 {{ palette[0] }}</h1>
        <p class="comment">这组颜色清爽、明亮，适合成为今天的主食。</p>

        <div class="score-row">
          <span>色彩评分</span>
          <strong>{{ score }}</strong>
        </div>

        <div class="palette-row" aria-label="本次颜色">
          <span
            v-for="color in palette"
            :key="color"
            class="swatch"
            :style="{ backgroundColor: color }"
          />
        </div>

        <div class="energy-card">
          <span>能量增加</span>
          <strong>+{{ energyGain }}</strong>
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

.page-nav a {
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

.palette-row {
  display: grid;
  grid-template-columns: repeat(5, minmax(34px, 1fr));
  gap: 10px;
}

.swatch {
  min-height: 54px;
  border-radius: 8px;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);
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

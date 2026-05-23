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
const energyPercent = computed(() =>
  Math.min(
    Math.round((displayPet.value.energy.current / displayPet.value.energy.max) * 100),
    100,
  ),
)
const channels = computed(() => [
  { key: 'r', label: '红能量', color: '#ff6b6b', value: displayPet.value.energy.r },
  { key: 'g', label: '绿能量', color: '#4ecdc4', value: displayPet.value.energy.g },
  { key: 'b', label: '蓝能量', color: '#5b7cfa', value: displayPet.value.energy.b },
])

onMounted(async () => {
  if (!sessionStore.isLoggedIn || petStore.petInfo) return

  try {
    await petStore.fetchProfile()
  } catch (err) {
    console.warn('[ProfileView] Profile fetch failed, using demo pet.', err)
  }
})
</script>

<template>
  <main class="profile-page" :style="{ '--accent-color': displayPet.color }">
    <nav class="page-nav">
      <RouterLink to="/">采集颜色</RouterLink>
      <RouterLink to="/result">最近投喂</RouterLink>
    </nav>

    <section class="profile-layout">
      <div class="profile-copy">
        <p class="section-label">小彩状态</p>
        <h1>{{ displayPet.name }}</h1>
        <p class="mood-line">
          第 {{ displayPet.stage + 1 }} 阶段 · {{ displayPet.mood }} · {{ energyPercent }}%
        </p>

        <div class="energy-meter" aria-label="总能量">
          <span :style="{ width: `${energyPercent}%` }" />
        </div>

        <div class="channel-list">
          <article v-for="channel in channels" :key="channel.key">
            <div>
              <strong>{{ channel.label }}</strong>
              <span>{{ channel.value }}</span>
            </div>
            <i
              :style="{
                '--channel-color': channel.color,
                width: `${Math.min(channel.value, displayPet.energy.max)}%`,
              }"
            />
          </article>
        </div>
      </div>

      <PetDisplay :pet="displayPet" size="hero" event="idle" />
    </section>
  </main>
</template>

<style scoped>
.profile-page {
  min-height: 100vh;
  padding: 28px;
  background:
    radial-gradient(circle at 78% 20%, color-mix(in srgb, var(--accent-color), transparent 74%), transparent 26%),
    linear-gradient(180deg, #ffffff, #f8f9fa);
  color: #252525;
}

.page-nav {
  width: min(1080px, 100%);
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

.profile-layout {
  width: min(1080px, 100%);
  min-height: calc(100vh - 102px);
  display: grid;
  grid-template-columns: minmax(320px, 1fr) minmax(280px, 0.92fr);
  align-items: center;
  gap: 58px;
  margin: 0 auto;
}

.profile-copy {
  display: grid;
  gap: 20px;
}

.section-label,
.mood-line {
  margin: 0;
}

.section-label {
  color: var(--accent-color);
  font-size: 13px;
  font-weight: 850;
}

h1 {
  margin: 0;
  font-size: clamp(44px, 7vw, 82px);
  line-height: 0.96;
  letter-spacing: 0;
}

.mood-line {
  color: #69645e;
  font-size: 17px;
  font-weight: 720;
}

.energy-meter {
  height: 18px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.84);
  box-shadow: inset 0 0 0 1px rgba(35, 35, 35, 0.08);
}

.energy-meter span {
  height: 100%;
  display: block;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--accent-color), #4ecdc4, #ffe66d);
}

.channel-list {
  display: grid;
  gap: 12px;
}

.channel-list article {
  display: grid;
  gap: 9px;
  padding: 14px;
  border: 1px solid rgba(31, 31, 31, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.74);
}

.channel-list div {
  display: flex;
  justify-content: space-between;
  gap: 18px;
}

.channel-list strong,
.channel-list span {
  font-size: 14px;
}

.channel-list i {
  height: 10px;
  border-radius: 999px;
  background: var(--channel-color);
}

@media (max-width: 760px) {
  .profile-page {
    padding: 18px;
  }

  .page-nav {
    justify-content: center;
  }

  .profile-layout {
    min-height: auto;
    grid-template-columns: 1fr;
    gap: 18px;
  }

  .profile-copy {
    order: 2;
  }

  h1 {
    font-size: 52px;
  }
}
</style>

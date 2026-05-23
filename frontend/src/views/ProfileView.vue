<script setup lang="ts">
import { computed, onMounted } from 'vue'
import PetDisplay from '@/components/PetDisplay.vue'
import {
  ALL_ACHIEVEMENTS,
  ALL_COLORS,
  AchievementCategoryColor,
  AchievementCategoryLabel,
  getGlobalProgress,
} from '@/utils/constants'
import { usePaletteStore } from '@/stores/palette'
import { usePetStore } from '@/stores/pet'
import { useSessionStore } from '@/stores/session'
import { createDemoPet } from '@/utils/demoPet'

const paletteStore = usePaletteStore()
const petStore = usePetStore()
const sessionStore = useSessionStore()

const displayPet = computed(() => petStore.petInfo ?? createDemoPet(paletteStore.accentColor))
const collectedIds = computed(() => paletteStore.collectedColors.map((color) => color))
const progress = computed(() => getGlobalProgress(collectedIds.value))
const progressPercent = computed(() => Math.round((progress.value.collected / progress.value.total) * 100))
const stage = computed(() => {
  if (progressPercent.value >= 75) return 3
  if (progressPercent.value >= 40) return 2
  if (progressPercent.value >= 15) return 1
  return 0
})

const achievements = computed(() =>
  ALL_ACHIEVEMENTS.map((achievement, index) => ({
    ...achievement,
    unlocked: index < Math.min(ALL_ACHIEVEMENTS.length, Math.floor(progress.value.collected / 2)),
  })),
)

const unlockedCount = computed(() => achievements.value.filter((item) => item.unlocked).length)

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
  <section class="profile-page">
    <header class="profile-hero">
      <div class="identity">
        <p class="eyebrow">Profile</p>
        <h1>{{ sessionStore.session?.display_name || 'ColorPal 用户' }}</h1>
        <p>用颜色记录世界，养成你的专属色彩精灵。</p>
      </div>

      <PetDisplay :pet="displayPet" size="hero" event="idle" />
    </header>

    <section class="stats-grid" aria-label="个人统计">
      <article>
        <strong>{{ progress.collected }}</strong>
        <span>已收集</span>
      </article>
      <article>
        <strong>{{ progress.total }}</strong>
        <span>目标色</span>
      </article>
      <article>
        <strong>{{ unlockedCount }}</strong>
        <span>成就</span>
      </article>
      <article>
        <strong>{{ stage + 1 }}</strong>
        <span>精灵阶段</span>
      </article>
    </section>

    <section class="progress-panel">
      <div class="panel-header">
        <h2>色彩进度</h2>
        <span>{{ progressPercent }}%</span>
      </div>
      <div class="progress-track">
        <span :style="{ width: progressPercent + '%' }" />
      </div>
      <div class="rarity-grid">
        <div>
          <strong>{{ progress.common.collected }}/{{ progress.common.total }}</strong>
          <span>常见</span>
        </div>
        <div>
          <strong>{{ progress.rare.collected }}/{{ progress.rare.total }}</strong>
          <span>稀有</span>
        </div>
        <div>
          <strong>{{ progress.epic.collected }}/{{ progress.epic.total }}</strong>
          <span>史诗</span>
        </div>
        <div>
          <strong>{{ progress.legendary.collected }}/{{ progress.legendary.total }}</strong>
          <span>传说</span>
        </div>
      </div>
    </section>

    <section class="achievement-panel">
      <div class="panel-header">
        <h2>成就</h2>
        <span>{{ unlockedCount }}/{{ ALL_ACHIEVEMENTS.length }}</span>
      </div>

      <div class="achievement-list">
        <article
          v-for="item in achievements"
          :key="item.id"
          class="achievement-card"
          :class="{ unlocked: item.unlocked }"
        >
          <span class="achievement-mark" :style="{ backgroundColor: AchievementCategoryColor[item.category] }" />
          <div>
            <strong>{{ item.name }}</strong>
            <p>{{ item.description }}</p>
          </div>
          <small>{{ AchievementCategoryLabel[item.category] }}</small>
        </article>
      </div>
    </section>
  </section>
</template>

<style scoped>
.profile-page {
  min-height: 100vh;
  padding: 112px max(24px, calc((100vw - 1080px) / 2)) 72px;
  background: #fbfbfa;
  color: #202020;
}

.profile-hero {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 32px;
  margin-bottom: 20px;
  padding: 28px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06);
}

.eyebrow,
h1,
h2,
p {
  margin: 0;
}

.eyebrow {
  color: var(--accent-color, #ff6b6b);
  font-size: 13px;
  font-weight: 850;
  text-transform: uppercase;
}

h1 {
  margin-top: 8px;
  font-size: 42px;
  letter-spacing: 0;
}

.identity p {
  margin-top: 12px;
  color: #666;
  line-height: 1.7;
}

.stats-grid,
.rarity-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.stats-grid article,
.rarity-grid div {
  display: grid;
  gap: 6px;
  padding: 18px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: #fff;
}

.stats-grid strong {
  color: var(--accent-color, #ff6b6b);
  font-size: 30px;
}

.stats-grid span,
.rarity-grid span {
  color: #777;
  font-size: 13px;
  font-weight: 700;
}

.progress-panel,
.achievement-panel {
  margin-top: 20px;
  padding: 22px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: #fff;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.panel-header h2 {
  font-size: 22px;
}

.panel-header span {
  color: var(--accent-color, #ff6b6b);
  font-weight: 850;
}

.progress-track {
  height: 10px;
  margin-bottom: 16px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(20, 20, 20, 0.08);
}

.progress-track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--accent-color, #ff6b6b);
}

.achievement-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.achievement-card {
  display: grid;
  grid-template-columns: 12px 1fr auto;
  align-items: center;
  gap: 12px;
  min-height: 84px;
  padding: 14px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: rgba(250, 250, 250, 0.72);
  opacity: 0.58;
}

.achievement-card.unlocked {
  background: #fff;
  opacity: 1;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.achievement-mark {
  width: 12px;
  height: 48px;
  border-radius: 999px;
}

.achievement-card strong {
  display: block;
  margin-bottom: 4px;
}

.achievement-card p,
.achievement-card small {
  color: #777;
  font-size: 13px;
  line-height: 1.5;
}

.achievement-card small {
  justify-self: end;
  white-space: nowrap;
}

@media (max-width: 760px) {
  .profile-page {
    padding: 30px 16px 106px;
  }

  .profile-hero {
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
    padding: 24px 18px;
  }

  h1 {
    font-size: 34px;
  }

  .stats-grid,
  .rarity-grid,
  .achievement-list {
    grid-template-columns: 1fr 1fr;
  }

  .achievement-card {
    grid-template-columns: 10px 1fr;
  }

  .achievement-card small {
    grid-column: 2;
    justify-self: start;
  }
}
</style>

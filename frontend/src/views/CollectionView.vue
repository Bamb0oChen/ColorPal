<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  ALL_COLORS,
  ColorFamily,
  ColorFamilyColor,
  ColorFamilyLabel,
  RarityColor,
  RarityLabel,
  RarityStars,
  getColorsByFamily,
} from '@/utils/constants'
import { usePaletteStore } from '@/stores/palette'

const paletteStore = usePaletteStore()
const devMode = ref(false)

onMounted(() => {
  paletteStore.clearNewlyUnlocked()
})

const collectedIds = computed(() => {
  const ids = new Set(paletteStore.collectedColorItems.map((c) => c.id))
  if (devMode.value) {
    ALL_COLORS.forEach((c) => ids.add(c.id))
  }
  return ids
})

const families = computed(() =>
  Object.values(ColorFamily).map((family) => {
    const colors = getColorsByFamily(family)
    const collected = colors.filter((color) => collectedIds.value.has(color.id)).length

    return {
      family,
      label: ColorFamilyLabel[family],
      color: ColorFamilyColor[family],
      colors,
      collected,
      total: colors.length,
    }
  }),
)

const collectedTotal = computed(() => collectedIds.value.size)
</script>

<template>
  <section class="collection-page">
    <header class="page-heading">
      <div>
        <p class="eyebrow">Collection</p>
        <h1>颜色图鉴</h1>
      </div>
      <div class="heading-actions">
        <div class="summary-pill">
          <strong>{{ collectedTotal }}</strong>
          <span>/ {{ ALL_COLORS.length }}</span>
        </div>
        <button
          class="dev-button"
          :class="{ active: devMode }"
          title="开发者模式：显示全部颜色"
          @click="devMode = !devMode"
        >
          Dev
        </button>
      </div>
    </header>

    <div v-if="devMode" class="dev-banner">
      开发者模式 — 所有颜色已解锁（仅前端展示）
    </div>

    <div class="family-list">
      <section v-for="group in families" :key="group.family" class="family-section">
        <header class="family-header">
          <div>
            <span class="family-mark" :style="{ backgroundColor: group.color }" />
            <h2>{{ group.label }}</h2>
          </div>
          <span>{{ group.collected }}/{{ group.total }}</span>
        </header>

        <div class="color-grid">
          <article
            v-for="color in group.colors"
            :key="color.id"
            class="color-card"
            :class="{
              collected: collectedIds.has(color.id),
              locked: !collectedIds.has(color.id),
            }"
          >
            <div class="color-sample-wrap">
              <span
                v-if="paletteStore.isNewlyUnlocked(color.id)"
                class="new-dot"
              />
              <div
                class="color-sample"
                :style="{
                  backgroundColor: collectedIds.has(color.id) ? color.hex : '#e8e8e8',
                  borderColor: collectedIds.has(color.id)
                    ? (color.hex === '#FFFFFF' ? '#ddd' : color.hex)
                    : '#d0d0d0',
                }"
              />
              <div v-if="!collectedIds.has(color.id)" class="lock-mask">
                <svg class="lock-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
              </div>
            </div>
            <div class="color-info">
              <strong>{{ collectedIds.has(color.id) ? color.name : '???' }}</strong>
              <span>{{ collectedIds.has(color.id) ? color.english : '未收集' }}</span>
            </div>
            <div class="rarity" :style="{ color: RarityColor[color.rarity] }">
              <span>{{ RarityLabel[color.rarity] }}</span>
              <span>{{ RarityStars[color.rarity] }}</span>
            </div>
          </article>
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.collection-page {
  min-height: 100vh;
  padding: 112px max(24px, calc((100vw - 1080px) / 2)) 72px;
  background: #fbfbfa;
  color: #202020;
}

.page-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}

.heading-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.eyebrow,
h1,
h2 {
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

.summary-pill {
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
  padding: 10px 14px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06);
}

.summary-pill strong {
  color: var(--accent-color, #ff6b6b);
  font-size: 28px;
}

.dev-button {
  height: 38px;
  padding: 0 14px;
  border: 1px solid rgba(20, 20, 20, 0.1);
  border-radius: 6px;
  background: #fff;
  color: #888;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  letter-spacing: 0.5px;
}

.dev-button.active {
  border-color: #ff6b6b;
  background: #ff6b6b;
  color: #fff;
}

.dev-banner {
  padding: 10px 16px;
  margin-bottom: 20px;
  border-radius: 8px;
  background: #fff3cd;
  color: #856404;
  font-size: 13px;
  font-weight: 700;
}

.family-list {
  display: grid;
  gap: 22px;
}

.family-section {
  display: grid;
  gap: 12px;
}

.family-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #666;
  font-weight: 750;
}

.family-header div {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.family-mark {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.family-header h2 {
  color: #252525;
  font-size: 19px;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.color-card {
  display: grid;
  grid-template-columns: 42px 1fr auto;
  align-items: center;
  gap: 12px;
  min-height: 74px;
  padding: 12px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
  color: #888;
}

.color-card.collected {
  background: #fff;
  color: #252525;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.color-sample-wrap {
  position: relative;
  width: 42px;
  height: 42px;
  flex-shrink: 0;
}

.color-sample {
  width: 42px;
  height: 42px;
  border: 1px solid;
  border-radius: 8px;
}

.lock-mask {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(2px);
}

.lock-icon {
  width: 18px;
  height: 18px;
  color: #999;
}

.new-dot {
  position: absolute;
  top: -3px;
  right: -3px;
  z-index: 5;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ff3b30;
  border: 2px solid #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.color-info {
  display: grid;
  gap: 3px;
  min-width: 0;
}

.color-info strong,
.color-info span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.color-info span,
.rarity {
  font-size: 12px;
}

.rarity {
  display: grid;
  justify-items: end;
  gap: 3px;
  font-weight: 800;
}

@media (max-width: 960px) {
  .color-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .collection-page {
    padding: 30px 16px 106px;
  }

  .page-heading {
    align-items: start;
  }

  h1 {
    font-size: 34px;
  }

  .color-grid {
    grid-template-columns: 1fr;
  }
}
</style>

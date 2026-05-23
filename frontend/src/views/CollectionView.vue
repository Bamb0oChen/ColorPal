<script setup lang="ts">
import { computed } from 'vue'
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

const collectedIds = computed(() => new Set(paletteStore.collectedColorItems.map((color) => color.id)))

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
      <div class="summary-pill">
        <strong>{{ collectedTotal }}</strong>
        <span>/ {{ ALL_COLORS.length }}</span>
      </div>
    </header>

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
            :class="{ collected: collectedIds.has(color.id) }"
          >
            <div
              class="color-sample"
              :style="{ backgroundColor: color.hex, borderColor: color.hex === '#FFFFFF' ? '#ddd' : color.hex }"
            />
            <div class="color-info">
              <strong>{{ color.name }}</strong>
              <span>{{ color.english }}</span>
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

.color-sample {
  width: 42px;
  height: 42px;
  border: 1px solid;
  border-radius: 8px;
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

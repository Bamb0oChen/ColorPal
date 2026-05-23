<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCollectionStore } from '@/stores/collection'
import {
  ALL_COLORS,
  ColorFamily,
  ColorFamilyLabel,
  ColorFamilyColor,
  Rarity,
  RarityLabel,
  RarityColor,
  RarityStars,
} from '@/utils/constants'
import type { ColorItem } from '@/utils/constants'
import ColorCard from '@/components/collection/ColorCard.vue'

const store = useCollectionStore()

const activeFamily = ref<string>('all')

const families = computed(() => [
  { id: 'all', name: '全部', color: '#636E72' },
  ...Object.values(ColorFamily).map((f) => ({
    id: f,
    name: ColorFamilyLabel[f as ColorFamily],
    color: ColorFamilyColor[f as ColorFamily],
  })),
])

const filteredColors = computed<ColorItem[]>(() => {
  if (activeFamily.value === 'all') return ALL_COLORS
  return ALL_COLORS.filter((c) => c.family === activeFamily.value)
})

const selectedColor = ref<ColorItem | null>(null)
const showDetail = ref(false)

const sortedColors = computed(() => {
  const order: Record<string, number> = {
    [Rarity.LEGENDARY]: 0,
    [Rarity.EPIC]: 1,
    [Rarity.RARE]: 2,
    [Rarity.COMMON]: 3,
  }
  return [...filteredColors.value].sort((a, b) => {
    const aCol = store.isCollected(a.id) ? 0 : 1
    const bCol = store.isCollected(b.id) ? 0 : 1
    if (aCol !== bCol) return aCol - bCol
    return (order[a.rarity] ?? 9) - (order[b.rarity] ?? 9)
  })
})

const openDetail = (colorId: string) => {
  const c = store.getColorDetail(colorId)
  if (c) {
    selectedColor.value = c
    showDetail.value = true
  }
}

const closeDetail = () => {
  showDetail.value = false
  selectedColor.value = null
}

onMounted(() => {
  store.fetchAll()
})
</script>

<template>
  <div class="collection-page">
    <!-- ====== 顶部总进度 ====== -->
    <section class="progress-hero">
      <div class="hero-left">
        <h1 class="page-title">色彩图鉴</h1>
        <p class="page-subtitle">收集你眼中的世界</p>
      </div>
      <div class="hero-right">
        <div class="big-number">{{ store.totalCollected }}</div>
        <div class="big-denom">/ {{ store.totalColors }}</div>
      </div>
    </section>

    <section class="progress-bar-wrap">
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: store.collectPercent + '%' }" />
      </div>
      <span class="progress-pct">{{ store.collectPercent }}%</span>
    </section>

    <!-- ====== 色系标签栏 ====== -->
    <section class="family-tabs">
      <button
        v-for="f in families"
        :key="f.id"
        class="family-tab"
        :class="{ active: activeFamily === f.id }"
        :style="activeFamily === f.id ? { borderBottomColor: f.color, color: f.color } : {}"
        @click="activeFamily = f.id"
      >
        <span class="tab-dot" :style="{ background: f.color }" />
        {{ f.name }}
      </button>
    </section>

    <!-- ====== 颜色网格 ====== -->
    <section class="color-grid-section">
      <div v-if="store.isLoading" class="loading-state">
        <div class="loading-spinner" />
        <span>加载图鉴中...</span>
      </div>

      <div v-else-if="store.error" class="error-state">
        <span>{{ store.error }}</span>
        <button class="retry-btn" @click="store.fetchAll()">重试</button>
      </div>

      <div v-else class="color-grid">
        <ColorCard
          v-for="c in sortedColors"
          :key="c.id"
          :color="c"
          :collected="store.isCollected(c.id)"
          @click="openDetail"
        />
      </div>
    </section>

    <!-- ====== 颜色详情弹窗 ====== -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showDetail && selectedColor" class="detail-overlay" @click.self="closeDetail">
          <div class="detail-panel">
            <div class="detail-swatch" :style="{ background: selectedColor.hex }">
              <span class="detail-hex">{{ selectedColor.hex }}</span>
              <span v-if="store.isCollected(selectedColor.id)" class="detail-collected-badge">已收集</span>
              <span v-else class="detail-collected-badge uncollected">未收集</span>
            </div>

            <div class="detail-info">
              <h2 class="detail-name">{{ selectedColor.name }}</h2>
              <p class="detail-english">{{ selectedColor.english }}</p>

              <div class="detail-tags">
                <span class="detail-tag family-tag" :style="{ background: ColorFamilyColor[selectedColor.family as ColorFamily] + '22', color: ColorFamilyColor[selectedColor.family as ColorFamily] }">
                  {{ ColorFamilyLabel[selectedColor.family as ColorFamily] }}
                </span>
                <span class="detail-tag rarity-tag" :style="{ background: RarityColor[selectedColor.rarity as Rarity] + '22', color: RarityColor[selectedColor.rarity as Rarity] }">
                  {{ RarityLabel[selectedColor.rarity as Rarity] }}
                  <template v-if="RarityStars[selectedColor.rarity as Rarity]">
                    {{ RarityStars[selectedColor.rarity as Rarity] }}
                  </template>
                </span>
              </div>
            </div>

            <button class="detail-close" @click="closeDetail">✕</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.collection-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 20px 12px 48px;
  background: #FFFAF7;
  min-height: 100vh;
}

/* ====== 进度头部 ====== */
.progress-hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 10px;
}

.page-title {
  font-size: 22px;
  font-weight: 800;
  color: #2D3436;
  margin: 0;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 12px;
  color: #B2BEC3;
  margin: 2px 0 0;
}

.hero-right {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.big-number {
  font-size: 28px;
  font-weight: 800;
  color: #FF7E67;
  line-height: 1;
}

.big-denom {
  font-size: 14px;
  color: #B2BEC3;
  font-weight: 500;
}

/* ====== 进度条 ====== */
.progress-bar-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.progress-track {
  flex: 1;
  height: 6px;
  background: #F0F0F0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FF7E67, #FFD700);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.progress-pct {
  font-size: 12px;
  font-weight: 700;
  color: #FF7E67;
  min-width: 36px;
  text-align: right;
}

/* ====== 色系标签栏 ====== */
.family-tabs {
  display: flex;
  gap: 2px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  margin-bottom: 12px;
  padding-bottom: 2px;
  margin-left: -12px;
  margin-right: -12px;
  padding-left: 12px;
  padding-right: 12px;
}

.family-tabs::-webkit-scrollbar {
  display: none;
}

.family-tab {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 6px 10px;
  border: none;
  background: transparent;
  font-size: 12px;
  font-weight: 500;
  color: #636E72;
  cursor: pointer;
  white-space: nowrap;
  border-bottom: 2px solid transparent;
  transition: all 0.15s;
  flex-shrink: 0;
}

.family-tab:hover {
  color: #2D3436;
}

.family-tab.active {
  font-weight: 700;
}

.tab-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ====== 颜色网格 ====== */
.color-grid-section {
  margin-bottom: 8px;
}

.color-grid {
  display: grid;
  gap: 6px;
}

/* ====== 加载/错误态 ====== */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #B2BEC3;
  font-size: 14px;
  gap: 12px;
}

.loading-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #F0F0F0;
  border-top-color: #FF7E67;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.retry-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 8px;
  background: #FF7E67;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

/* ====== 颜色详情弹窗 ====== */
.detail-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.detail-panel {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  width: 100%;
  max-width: 320px;
  position: relative;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.detail-swatch {
  width: 100%;
  aspect-ratio: 3/2;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 14px;
  position: relative;
}

.detail-hex {
  font-size: 13px;
  font-weight: 700;
  color: white;
  text-shadow: 0 1px 4px rgba(0,0,0,0.3);
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.detail-collected-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 3px 8px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
  background: rgba(255,255,255,0.9);
  color: #00B894;
}

.detail-collected-badge.uncollected {
  color: #B2BEC3;
}

.detail-info {
  padding: 14px 16px 18px;
}

.detail-name {
  font-size: 18px;
  font-weight: 700;
  color: #2D3436;
  margin: 0;
}

.detail-english {
  font-size: 12px;
  color: #B2BEC3;
  margin: 2px 0 10px;
}

.detail-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.detail-tag {
  padding: 3px 8px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
}

.detail-close {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(0,0,0,0.3);
  color: white;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.detail-close:hover {
  background: rgba(0,0,0,0.5);
}

/* 弹窗过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ================================================================
   响应式断点（移动端优先）
   ================================================================ */

/* 手机 - 小屏 (< 400px) */
@media (max-width: 399px) {
  .collection-page {
    padding: 14px 8px 40px;
  }
  .page-title { font-size: 18px; }
  .big-number { font-size: 24px; }
  .big-denom { font-size: 12px; }
  .color-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
  }
  .family-tab {
    font-size: 11px;
    padding: 5px 8px;
  }
  .detail-panel {
    max-width: 280px;
  }
}

/* 手机 - 常规 (400px - 479px) */
@media (min-width: 400px) and (max-width: 479px) {
  .collection-page {
    padding: 16px 10px 40px;
  }
  .color-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }
}

/* 小平板 / 大手机 (480px - 599px) */
@media (min-width: 480px) and (max-width: 599px) {
  .collection-page {
    padding: 20px 14px 44px;
  }
  .page-title { font-size: 20px; }
  .big-number { font-size: 26px; }
  .color-grid {
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
  }
  .family-tab {
    font-size: 12px;
    padding: 6px 12px;
  }
}

/* 平板 (600px - 767px) */
@media (min-width: 600px) and (max-width: 767px) {
  .collection-page {
    padding: 24px 20px 48px;
  }
  .color-grid {
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
  }
  .progress-hero { margin-bottom: 14px; }
  .family-tabs {
    gap: 4px;
    margin-bottom: 16px;
  }
}

/* 桌面 (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  .collection-page {
    padding: 28px 24px 56px;
  }
  .page-title { font-size: 24px; }
  .page-subtitle { font-size: 13px; }
  .big-number { font-size: 32px; }
  .progress-track { height: 8px; }
  .color-grid {
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
  }
  .family-tab {
    font-size: 13px;
    padding: 8px 14px;
  }
  .detail-panel {
    max-width: 340px;
  }
}

/* 宽桌面 (1024px+) */
@media (min-width: 1024px) {
  .collection-page {
    padding: 32px 32px 64px;
  }
  .page-title {
    font-size: 26px;
  }
  .page-subtitle {
    font-size: 14px;
  }
  .big-number { font-size: 34px; }
  .big-denom { font-size: 16px; }
  .progress-hero { margin-bottom: 16px; }
  .progress-bar-wrap { margin-bottom: 20px; }
  .progress-track { height: 8px; }
  .progress-pct { font-size: 13px; }
  .color-grid {
    grid-template-columns: repeat(8, 1fr);
    gap: 14px;
  }
  .family-tabs {
    gap: 6px;
    margin-bottom: 20px;
  }
  .family-tab {
    font-size: 14px;
    padding: 8px 16px;
  }
  .detail-panel {
    max-width: 360px;
  }
  .detail-name { font-size: 20px; }
  .detail-swatch { padding: 16px; }
  .detail-info { padding: 16px 20px 20px; }
  .detail-hex { font-size: 14px; }
}
</style>

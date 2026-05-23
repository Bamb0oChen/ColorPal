<script setup lang="ts">
import { computed } from 'vue'
import type { ColorItem } from '@/utils/constants'
import { Rarity, RarityLabel, RarityColor, RarityStars } from '@/utils/constants'

const props = defineProps<{
  color: ColorItem
  collected: boolean
}>()

const emit = defineEmits<{
  click: [colorId: string]
}>()

const rarityStyle = computed(() => {
  if (!props.collected) return {}
  const borderColor = RarityColor[props.color.rarity as Rarity]
  const borderWidth = props.color.rarity === Rarity.LEGENDARY ? 2 : 1.5
  return {
    borderColor,
    borderWidth: `${borderWidth}px`,
  }
})

const starDisplay = computed(() => {
  if (!props.collected) return ''
  return RarityStars[props.color.rarity as Rarity]
})

const glowStyle = computed(() => {
  if (!props.collected) return {}
  if (props.color.rarity !== Rarity.LEGENDARY) return {}
  return {
    boxShadow: `0 0 12px ${RarityColor[Rarity.LEGENDARY]}66`,
  }
})

const rarityLabel = computed(() => {
  if (!props.collected) return ''
  return RarityLabel[props.color.rarity as Rarity]
})
</script>

<template>
  <div
    class="color-card"
    :class="{ collected, legendary: collected && color.rarity === 'legendary' }"
    :style="glowStyle"
    @click="emit('click', color.id)"
  >
    <!-- 色块 -->
    <div class="swatch" :style="{ ...rarityStyle, background: collected ? color.hex : '#E8E8E8' }">
      <!-- 未收集时显示问号 -->
      <span v-if="!collected" class="uncollected-mark">?</span>
      <!-- 稀有度星标 -->
      <span v-if="starDisplay" class="rarity-stars" :style="{ color: RarityColor[color.rarity as Rarity] }">
        {{ starDisplay }}
      </span>
      <!-- 传说额外光晕 -->
      <div v-if="collected && color.rarity === 'legendary'" class="legend-glow" />
    </div>

    <!-- 颜色名称 -->
    <div class="color-name" :class="{ uncollected: !collected }">
      {{ color.name }}
    </div>

    <!-- 稀有度标签 -->
    <div v-if="collected && color.rarity !== 'common'" class="rarity-label" :style="{ color: RarityColor[color.rarity as Rarity] }">
      {{ rarityLabel }}
    </div>
  </div>
</template>

<style scoped>
.color-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: transform 0.15s ease;
  border-radius: 10px;
  padding: 6px;
}

.color-card:hover {
  transform: translateY(-2px);
}

.color-card:active {
  transform: scale(0.96);
}

.swatch {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: 10px;
  border: 1.5px solid #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  overflow: hidden;
}

.collected .swatch {
  border-style: solid;
}

.uncollected-mark {
  font-size: 20px;
  font-weight: 700;
  color: #CCC;
  user-select: none;
}

.rarity-stars {
  position: absolute;
  top: 3px;
  right: 4px;
  font-size: 10px;
  line-height: 1;
  text-shadow: 0 0 3px rgba(0,0,0,0.3);
}

.legend-glow {
  position: absolute;
  inset: -2px;
  border-radius: 12px;
  background: radial-gradient(circle at 50% 50%, rgba(255,215,0,0.15), transparent 70%);
  pointer-events: none;
}

.color-name {
  font-size: 11px;
  color: #2D3436;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  text-align: center;
}

.color-name.uncollected {
  color: #B2BEC3;
}

.rarity-label {
  font-size: 9px;
  font-weight: 600;
  line-height: 1;
}

/* 响应式：小屏幕缩小间距 */
@media (max-width: 400px) {
  .color-card {
    padding: 4px;
  }
  .color-name {
    font-size: 10px;
  }
}
</style>

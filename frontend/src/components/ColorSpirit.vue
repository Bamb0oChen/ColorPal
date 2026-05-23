<template>
  <div class="spirit-wrap" :style="{ width: size + 'px' }">
    <svg
      :width="size"
      :height="size * 1.2"
      viewBox="0 0 200 240"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <radialGradient :id="gradId" cx="50%" cy="40%" r="60%">
          <stop offset="0%" :stop-color="lightColor" />
          <stop offset="70%" :stop-color="mainColor" />
          <stop offset="100%" :stop-color="darkColor" />
        </radialGradient>
        <radialGradient :id="glowId" cx="50%" cy="50%" r="50%">
          <stop offset="0%" :stop-color="mainColor" stop-opacity="0.3" />
          <stop offset="100%" :stop-color="mainColor" stop-opacity="0" />
        </radialGradient>
      </defs>

      <!-- 光晕 -->
      <ellipse cx="100" cy="115" rx="65" ry="55" :fill="`url(#${glowId})`" opacity="0.6">
        <animate attributeName="opacity" values="0.4;0.7;0.4" dur="3s" repeatCount="indefinite" />
      </ellipse>

      <!-- 翅膀（成体+） -->
      <g v-if="stage >= 1" :opacity="stage >= 2 ? 1 : 0.6">
        <ellipse cx="42" cy="125" rx="26" ry="14" :fill="lightColor" fill-opacity="0.35" transform="rotate(-25, 100, 130)" />
        <ellipse cx="158" cy="125" rx="26" ry="14" :fill="lightColor" fill-opacity="0.35" transform="rotate(25, 100, 130)" />
      </g>

      <!-- 主体：火焰/水滴形 -->
      <path
        d="M 100 38 C 142 38, 160 78, 156 118 C 152 152, 128 178, 100 188 C 72 178, 48 152, 44 118 C 40 78, 58 38, 100 38 Z"
        :fill="`url(#${gradId})`"
      />

      <!-- 身体高光 -->
      <path
        d="M 88 58 C 100 54, 118 56, 125 66 C 128 71, 122 64, 110 60 C 98 56, 90 60, 88 58 Z"
        fill="white" fill-opacity="0.15"
      />

      <!-- 左眼 -->
      <ellipse cx="85" cy="92" rx="3.5" ry="4.5" fill="#2D3436">
        <animate attributeName="ry" :values="eyeAnim" dur="4s" repeatCount="indefinite" />
      </ellipse>
      <!-- 右眼 -->
      <ellipse cx="115" cy="92" rx="3.5" ry="4.5" fill="#2D3436">
        <animate attributeName="ry" :values="eyeAnim" dur="4s" repeatCount="indefinite" />
      </ellipse>

      <!-- 高光 -->
      <circle cx="83.5" cy="89" r="1.5" fill="white" fill-opacity="0.8" />
      <circle cx="113.5" cy="89" r="1.5" fill="white" fill-opacity="0.8" />

      <!-- 嘴巴 -->
      <path :d="mouthPath" fill="none" stroke="#2D3436" stroke-width="2" stroke-linecap="round" />

      <!-- 腮红 -->
      <ellipse v-if="mood === 'happy'" cx="72" cy="106" rx="6" ry="3.5" :fill="mainColor" fill-opacity="0.2" />
      <ellipse v-if="mood === 'happy'" cx="128" cy="106" rx="6" ry="3.5" :fill="mainColor" fill-opacity="0.2" />

      <!-- 触角（小火焰尖） -->
      <path d="M 100 38 Q 96 26 100 18 Q 104 26 100 38 Z" :fill="`url(#${gradId})`" />

      <!-- 触角球 -->
      <circle cx="100" cy="16" :r="antSize" :fill="antennaColor">
        <animate attributeName="r" :values="`${antSize};${antSize + 1};${antSize}`" dur="2s" repeatCount="indefinite" />
      </circle>

      <!-- 皇冠 -->
      <g v-if="stage >= 2">
        <!-- 成熟态 -->
        <g v-if="stage === 2" opacity="0.95">
          <path d="M 85 28 L 90 14 L 95 22 L 100 12 L 105 22 L 110 14 L 115 28 Z" fill="#A29BFE" />
        </g>
        <!-- 完全体 -->
        <g v-else opacity="0.95">
          <path d="M 80 30 L 86 8 L 93 18 L 100 4 L 107 18 L 114 8 L 120 30 Z" fill="#FFD700" />
          <circle cx="100" cy="4" r="2" fill="#FFD700" />
          <circle cx="86" cy="8" r="1.5" fill="#FFD700" />
          <circle cx="114" cy="8" r="1.5" fill="#FFD700" />
        </g>
      </g>

      <!-- 漂浮粒子 -->
      <circle v-for="(p, i) in particles" :key="i"
        :cx="p.x" :cy="p.y" :r="p.r"
        :fill="lightColor" fill-opacity="0.5"
      >
        <animate attributeName="cy" :values="`${p.y};${p.y - 10};${p.y}`" :dur="`${p.dur}s`" :begin="`${p.delay}s`" repeatCount="indefinite" />
      </circle>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  color?: string
  size?: number
  mood?: 'happy' | 'neutral' | 'sad'
  stage?: number
}>(), {
  color: '#FF7E67',
  size: 200,
  mood: 'happy',
  stage: 0,
})

const gradId = `sg-${Math.random().toString(36).slice(2, 8)}`
const glowId = `sg-g-${Math.random().toString(36).slice(2, 8)}`

const mainColor = computed(() => props.color)
const lightColor = computed(() => lighten(props.color, 35))
const darkColor = computed(() => darken(props.color, 25))

const antennaColor = computed(() => {
  if (props.stage >= 3) return '#FFD700'
  if (props.stage >= 2) return '#A29BFE'
  if (props.stage >= 1) return '#74B9FF'
  return lighten(props.color, 35)
})

const antSize = computed(() => props.stage >= 3 ? 6 : 4.5)

const mouthPath = computed(() => {
  if (props.mood === 'happy') return 'M 93 104 Q 100 113 107 104'
  if (props.mood === 'sad') return 'M 94 112 Q 100 104 106 112'
  return 'M 95 106 Q 100 109 105 106'
})

const eyeAnim = computed(() => {
  if (props.mood === 'sad') return '6.5;6.5;6.5'
  return '4.5;1.5;4.5'
})

const particles = [
  { x: 75, y: 162, r: 2.5, dur: 3, delay: 0 },
  { x: 125, y: 167, r: 2.5, dur: 3.5, delay: 0.5 },
  { x: 100, y: 175, r: 2, dur: 2.8, delay: 1 },
]

function hexToRgb(hex: string) {
  const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return m ? { r: parseInt(m[1], 16), g: parseInt(m[2], 16), b: parseInt(m[3], 16) } : { r: 255, g: 126, b: 103 }
}

function lighten(hex: string, pct: number) {
  const { r, g, b } = hexToRgb(hex)
  const f = 1 + pct / 100
  return toHex(Math.min(255, Math.round(r * f)), Math.min(255, Math.round(g * f)), Math.min(255, Math.round(b * f)))
}

function darken(hex: string, pct: number) {
  const { r, g, b } = hexToRgb(hex)
  const f = 1 - pct / 100
  return toHex(Math.round(r * f), Math.round(g * f), Math.round(b * f))
}

function toHex(r: number, g: number, b: number) {
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`
}
</script>

<style scoped>
.spirit-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>

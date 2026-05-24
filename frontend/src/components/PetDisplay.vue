<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as PIXI from 'pixi.js'
import type {
  Live2DModel as Live2DModelType,
  MotionPriority as MotionPriorityType,
} from 'pixi-live2d-display/cubism2'
import type { PetInfo } from '@/types/pet'
import {
  cubism2RuntimeScript,
  defaultPetModel,
  makeModelSettings,
  type PetDisplayEvent,
  type PetDisplaySize,
} from '@/utils/live2d'

const props = withDefaults(
  defineProps<{
    pet: PetInfo
    size?: PetDisplaySize
    interactive?: boolean
    event?: PetDisplayEvent
    modelPath?: string
    showStats?: boolean
  }>(),
  {
    size: 'hero',
    interactive: true,
    event: 'idle',
    modelPath: defaultPetModel,
    showStats: true,
  },
)

type LoadState = 'loading' | 'ready' | 'failed'

declare global {
  interface Window {
    PIXI?: typeof PIXI
    Live2D?: unknown
  }
}

let runtimePromise: Promise<void> | null = null
let live2dModulePromise: Promise<typeof import('pixi-live2d-display/cubism2')> | null = null

const MOTION_PRIORITY = {
  IDLE: 1,
  NORMAL: 2,
  FORCE: 3,
} as const

const canvasHost = ref<HTMLDivElement | null>(null)
const loadState = ref<LoadState>('loading')
const app = ref<PIXI.Application | null>(null)
const model = ref<Live2DModelType | null>(null)
let resizeObserver: ResizeObserver | null = null

const accentColor = computed(() => props.pet.color || '#ff6b6b')
const energyPercent = computed(() =>
  Math.min(Math.round((props.pet.energy.current / props.pet.energy.max) * 100), 100),
)
const stageLevel = computed(() => Math.min(Math.max(props.pet.stage + 1, 1), 4))
const statusText = computed(() => {
  if (props.pet.mood === 'happy') return '今天吃得很开心'
  if (props.pet.mood === 'sad') return '想再尝一点颜色'
  return '正在慢慢消化'
})
const energyChannels = computed(() => [
  { key: 'r', label: 'R', color: '#ff6b6b', value: props.pet.energy.r },
  { key: 'g', label: 'G', color: '#4ecdc4', value: props.pet.energy.g },
  { key: 'b', label: 'B', color: '#5b7cfa', value: props.pet.energy.b },
])

onMounted(async () => {
  await nextTick()
  await mountLive2d()
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  resizeObserver = null
  model.value?.destroy({ children: true })
  model.value = null
  app.value?.destroy(true, { children: true })
  app.value = null
})

watch(
  () => props.event,
  async (event) => {
    if (loadState.value !== 'ready') return
    await playEventMotion(event)
  },
)

watch(
  () => props.pet.mood,
  async (mood) => {
    if (loadState.value !== 'ready') return
    if (mood === 'happy') await playMotion('shake')
  },
)

async function mountLive2d() {
  if (!canvasHost.value) return

  loadState.value = 'loading'

  try {
    window.PIXI = PIXI
    const { Live2DModel, MotionPreloadStrategy } = await loadLive2dModule()
    Live2DModel.registerTicker(PIXI.Ticker)

    const pixiApp = new PIXI.Application({
      antialias: true,
      autoDensity: true,
      backgroundAlpha: 0,
      resolution: window.devicePixelRatio || 1,
    })

    app.value = pixiApp
    canvasHost.value.appendChild(pixiApp.view as HTMLCanvasElement)

    const settings = await makeModelSettings(props.pet.color)
    const live2dModel = await Live2DModel.from(settings, {
      autoInteract: props.interactive,
      motionPreload: MotionPreloadStrategy.IDLE,
    })

    model.value = live2dModel
    live2dModel.anchor.set(0.5, 0.5)
    live2dModel.on('hit', async (hitAreas: string[]) => {
      if (hitAreas.includes('body')) await playMotion('tap_body')
    })

    pixiApp.stage.addChild(live2dModel)
    fitModel()
    observeSize()
    await playMotion('idle', MOTION_PRIORITY.IDLE)
    loadState.value = 'ready'
  } catch (err) {
    console.warn('[PetDisplay] Live2D load failed, using static fallback.', err)
    loadState.value = 'failed'
  }
}

function observeSize() {
  if (!canvasHost.value) return

  resizeObserver = new ResizeObserver(() => fitModel())
  resizeObserver.observe(canvasHost.value)
}

function fitModel() {
  if (!canvasHost.value || !app.value || !model.value) return

  const rect = canvasHost.value.getBoundingClientRect()
  const width = Math.max(Math.round(rect.width), 1)
  const height = Math.max(Math.round(rect.height), 1)

  app.value.renderer.resize(width, height)
  model.value.scale.set(1)

  const scaleMultiplier = props.showStats ? 1.5 : 1.55
  const scale =
    Math.min((width * 0.84) / model.value.width, (height * 0.86) / model.value.height) *
    scaleMultiplier
  model.value.scale.set(scale)
  model.value.x = width / 2
  model.value.y = height * (props.showStats ? 0.93 : 1.08)
}

async function playEventMotion(event: PetDisplayEvent) {
  if (event === 'success' || event === 'evolve') {
    await playMotion('shake', MOTION_PRIORITY.FORCE)
    return
  }

  if (event === 'tap' || event === 'feeding') {
    await playMotion('tap_body', MOTION_PRIORITY.FORCE)
  }
}

async function playMotion(
  group: 'idle' | 'shake' | 'tap_body',
  priority: MotionPriorityType = MOTION_PRIORITY.NORMAL as MotionPriorityType,
) {
  try {
    await model.value?.motion(group, undefined, priority)
  } catch (err) {
    console.warn(`[PetDisplay] Motion ${group} failed.`, err)
  }
}

async function loadLive2dModule() {
  await loadCubism2Runtime()
  if (!live2dModulePromise) {
    live2dModulePromise = import('pixi-live2d-display/cubism2')
  }

  return live2dModulePromise
}

async function loadCubism2Runtime() {
  if (window.Live2D) return
  if (runtimePromise) {
    await runtimePromise
    return
  }

  runtimePromise = new Promise((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>(
      `script[src="${cubism2RuntimeScript}"]`,
    )

    if (existing) {
      existing.addEventListener('load', () => resolve(), { once: true })
      existing.addEventListener('error', () => reject(new Error('Cubism 2 runtime failed')), {
        once: true,
      })
      return
    }

    const script = document.createElement('script')
    script.src = cubism2RuntimeScript
    script.async = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('Cubism 2 runtime failed'))
    document.head.appendChild(script)
  })

  await runtimePromise
}
</script>

<template>
  <section
    class="pet-display"
    :class="[
      `is-${size}`,
      `mood-${pet.mood}`,
      `state-${loadState}`,
      showStats ? 'has-stats' : 'is-visual-only',
    ]"
    :style="{ '--pet-accent': accentColor }"
    aria-label="小彩"
  >
    <div class="aura" />
    <div class="stage-orbit" aria-hidden="true">
      <span v-for="item in stageLevel" :key="item" />
    </div>

    <div class="live2d-frame">
      <div ref="canvasHost" class="canvas-host" />
      <div v-if="loadState !== 'ready'" class="fallback-shell" aria-hidden="true">
        <div class="fallback-bowl" />
        <div class="fallback-face">
          <span />
          <span />
        </div>
      </div>
    </div>

    <div class="color-drops" aria-hidden="true">
      <span />
      <span />
      <span />
    </div>

    <div v-if="showStats" class="pet-status">
      <div>
        <p class="pet-name">{{ pet.name }}</p>
        <p class="pet-caption">{{ statusText }}</p>
      </div>
      <strong>{{ energyPercent }}%</strong>
    </div>

    <div v-if="showStats" class="energy-beads" aria-label="RGB 能量">
      <span
        v-for="channel in energyChannels"
        :key="channel.key"
        :style="{
          '--bead-color': channel.color,
          '--bead-level': `${(Math.min(channel.value, pet.energy.max) / pet.energy.max) * 100}%`,
        }"
      >
        {{ channel.label }}
      </span>
    </div>
  </section>
</template>

<style scoped>
.pet-display {
  position: relative;
  width: min(48vw, 360px);
  min-width: 220px;
  aspect-ratio: 0.74;
  display: grid;
  grid-template-rows: minmax(0, 1fr);
  place-items: center;
  isolation: isolate;
  color: #282828;
  filter: drop-shadow(0 22px 34px color-mix(in srgb, var(--pet-accent), transparent 72%));
}

.pet-display.is-visual-only {
  aspect-ratio: 0.86;
}

.pet-display.has-stats {
  grid-template-rows: minmax(0, 1fr) auto auto;
}

.pet-display.is-compact {
  width: min(34vw, 220px);
  min-width: 164px;
}

.pet-display.is-avatar {
  width: min(24vw, 168px);
  min-width: 132px;
  filter: drop-shadow(0 14px 22px color-mix(in srgb, var(--pet-accent), transparent 78%));
}

.pet-display.is-panel {
  width: min(42vw, 300px);
  min-width: 210px;
}

.pet-display.is-visual-only {
  aspect-ratio: 0.86;
}

.aura {
  position: absolute;
  inset: 8% 4% 22%;
  z-index: -2;
  border-radius: 50%;
  background:
    radial-gradient(circle at 50% 42%, color-mix(in srgb, var(--pet-accent), white 72%), transparent 58%),
    radial-gradient(circle at 72% 24%, rgba(255, 230, 109, 0.54), transparent 20%);
  opacity: 0.9;
}

.stage-orbit {
  position: absolute;
  inset: 12% 18% auto;
  height: 52px;
  z-index: 2;
  pointer-events: none;
}

.stage-orbit span {
  position: absolute;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: color-mix(in srgb, var(--pet-accent), white 28%);
  box-shadow: 0 0 0 5px rgba(255, 255, 255, 0.56);
}

.stage-orbit span:nth-child(1) {
  left: 8%;
  top: 24px;
}

.stage-orbit span:nth-child(2) {
  left: 34%;
  top: 4px;
}

.stage-orbit span:nth-child(3) {
  right: 34%;
  top: 8px;
}

.stage-orbit span:nth-child(4) {
  right: 8%;
  top: 26px;
}

.live2d-frame {
  position: relative;
  width: 100%;
  min-height: 0;
  align-self: stretch;
  justify-self: stretch;
}

.is-visual-only .aura {
  inset: 10%;
  opacity: 0.62;
}

.is-visual-only .stage-orbit,
.is-visual-only .color-drops {
  display: none;
}

.canvas-host {
  position: absolute;
  inset: 0;
}

.canvas-host :deep(canvas) {
  width: 100%;
  height: 100%;
  display: block;
  transform: scaleY(1.30);
  transform-origin: 50% 0%;
}

.fallback-shell {
  position: absolute;
  left: 50%;
  top: 48%;
  width: 56%;
  aspect-ratio: 0.84;
  border-radius: 48% 48% 34% 34%;
  background:
    radial-gradient(circle at 38% 28%, rgba(255, 255, 255, 0.96), transparent 16%),
    linear-gradient(180deg, #fffdf9, color-mix(in srgb, var(--pet-accent), white 86%));
  box-shadow:
    inset 0 -14px 24px rgba(52, 38, 31, 0.08),
    0 22px 38px rgba(32, 32, 32, 0.1);
  transform: translate(-50%, -50%);
  animation: breathe 3.2s ease-in-out infinite;
}

.fallback-bowl {
  position: absolute;
  left: 50%;
  bottom: 8%;
  width: 82%;
  height: 28%;
  border-radius: 12px 12px 54px 54px;
  background: color-mix(in srgb, var(--pet-accent), #8d2c2c 34%);
  transform: translateX(-50%);
}

.fallback-face {
  position: absolute;
  left: 50%;
  top: 34%;
  width: 52px;
  display: flex;
  justify-content: space-between;
  transform: translateX(-50%);
}

.fallback-face span {
  width: 10px;
  height: 13px;
  border-radius: 999px;
  background: #2a2524;
}

.color-drops {
  position: absolute;
  inset: auto 11% 25%;
  height: 92px;
  z-index: 3;
  pointer-events: none;
}

.color-drops span {
  position: absolute;
  width: 14px;
  height: 22px;
  border-radius: 999px 999px 999px 4px;
  background: var(--pet-accent);
  opacity: 0.78;
  transform: rotate(35deg);
  animation: drip 3.8s ease-in-out infinite;
}

.color-drops span:nth-child(1) {
  left: 14%;
  top: 22%;
}

.color-drops span:nth-child(2) {
  left: 46%;
  top: 4%;
  width: 10px;
  height: 18px;
  animation-delay: 420ms;
}

.color-drops span:nth-child(3) {
  right: 14%;
  top: 30%;
  background: #4ecdc4;
  animation-delay: 840ms;
}

.pet-status {
  width: min(100%, 292px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 10px 12px;
  border: 1px solid rgba(32, 32, 32, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(14px);
}

.pet-name,
.pet-caption {
  margin: 0;
}

.pet-name {
  font-size: 15px;
  font-weight: 850;
}

.pet-caption {
  margin-top: 3px;
  color: #6d6762;
  font-size: 12px;
}

.pet-status strong {
  color: var(--pet-accent);
  font-size: 18px;
}

.energy-beads {
  width: min(100%, 292px);
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-top: 8px;
}

.energy-beads span {
  height: 30px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background:
    linear-gradient(
      90deg,
      color-mix(in srgb, var(--bead-color), white 18%) var(--bead-level),
      rgba(255, 255, 255, 0.78) 0
    );
  box-shadow: inset 0 0 0 1px rgba(36, 36, 36, 0.08);
  color: #252525;
  font-size: 12px;
  font-weight: 800;
}

.mood-happy .aura {
  opacity: 1;
}

.mood-sad .aura {
  opacity: 0.62;
  filter: saturate(0.72);
}

.state-ready .fallback-shell {
  display: none;
}

@keyframes breathe {
  0%,
  100% {
    transform: translate(-50%, -50%) translateY(0);
  }

  50% {
    transform: translate(-50%, -50%) translateY(-8px);
  }
}

@keyframes drip {
  0%,
  100% {
    transform: translateY(0) rotate(35deg);
  }

  50% {
    transform: translateY(8px) rotate(35deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .fallback-shell,
  .color-drops span {
    animation: none;
  }
}

@media (max-width: 760px) {
  .pet-display,
  .pet-display.is-panel {
    width: min(86vw, 320px);
  }

  .pet-display.is-compact {
    width: min(58vw, 220px);
  }

  .pet-display.is-avatar {
    width: min(42vw, 160px);
    min-width: 128px;
  }
}
</style>
